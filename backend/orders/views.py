from datetime import timedelta

from django.db import transaction
from django.db.models import Count, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from establishments.models import Establishment, Table
from products.models import Product
from shared.decorators import parse_json, require_http_methods
from users.decorators import auth_required

from .models import Order, OrderDetail
from .serializers import OrderDetailSerializer, OrderSerializer

# ──────────────────────────────────────────────
# Helpers privados
# ──────────────────────────────────────────────


def _get_est_ids_by_role(user, role):
    """Devuelve una lista plana con los IDs de establecimientos donde el usuario ejerce el rol indicado."""
    return list(
        user.manages.filter(role=role, end_date__isnull=True).values_list(
            'establishment_id', flat=True
        )
    )


def _get_primary_establishment(user, role):
    """Devuelve el establecimiento principal del usuario para un rol dado, o None."""
    est_ids = _get_est_ids_by_role(user, role)
    if not est_ids:
        return None
    return Establishment.objects.get(pk=est_ids[0])


def _list_orders_for_role(request, role):
    """Listado de pedidos filtrado por rol, establecimiento y rango de tiempo."""
    allowed_est_ids = _get_est_ids_by_role(request.user, role)
    if not allowed_est_ids:
        return JsonResponse([], safe=False)

    queryset = Order.objects.filter(establishment_id__in=allowed_est_ids).select_related(
        'table', 'establishment'
    )

    requested_est_id = request.GET.get('establishment_id')

    if requested_est_id and requested_est_id.isdigit():
        parsed_est_id = int(requested_est_id)
        if parsed_est_id in allowed_est_ids:
            queryset = queryset.filter(establishment_id=parsed_est_id)

    requested_days = request.GET.get('days')

    if requested_days and requested_days.isdigit():
        time_limit = timezone.now() - timedelta(days=int(requested_days))
        queryset = queryset.filter(placed_at__gte=time_limit)

    orders_sorted = queryset.order_by('-placed_at')
    return OrderSerializer(orders_sorted, request=request).json_response()


def _get_order_details_for_role(request, order_id, role):
    """Devuelve los detalles de un pedido verificando que pertenece a un establecimiento del rol."""
    est_ids = _get_est_ids_by_role(request.user, role)
    order = get_object_or_404(Order, pk=order_id, establishment_id__in=est_ids)

    order_details = order.details.select_related('product')
    return OrderDetailSerializer(order_details, request=request).json_response()


def _advance_order(request, order_id, role):
    """Avanza el estado: INITIATED → IN_PROGRESS → DONE."""
    est_ids = _get_est_ids_by_role(request.user, role)
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    try:
        order = Order.objects.get(id=order_id, establishment_id__in=est_ids)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Pedido no encontrado.'}, status=404)

    if order.status == Order.Status.INITIATED:
        order.status = Order.Status.IN_PROGRESS
    elif order.status == Order.Status.IN_PROGRESS:
        order.status = Order.Status.DONE
        order.closed_at = timezone.now()
    else:
        return JsonResponse({'error': 'Este pedido no se puede avanzar.'}, status=400)

    order.save()
    return JsonResponse(
        {
            'message': f'Pedido actualizado a "{order.get_status_display()}".',
            'status': order.status,
            'status_display': order.get_status_display(),
        }
    )


def _get_active_order_for_table(table, establishment):
    """Devuelve el pedido activo (no pagado) de una mesa, o None."""
    return (
        Order.objects.filter(
            table=table,
            establishment=establishment,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE],
        )
        .exclude(paid=True)
        .first()
    )


# ──────────────────────────────────────────────
# Manager: Pedidos
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
def list_manager_orders(request) -> JsonResponse:
    return _list_orders_for_role(request, 'manager')


@require_http_methods('GET')
@auth_required
def get_order_details(request, order_id: int) -> JsonResponse:
    return _get_order_details_for_role(request, order_id, 'manager')


# ──────────────────────────────────────────────
# Waiter: Pedidos
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
def list_waiter_orders(request) -> JsonResponse:
    return _list_orders_for_role(request, 'waiter')


@require_http_methods('GET')
@auth_required
def get_waiter_order_details(request, order_id: int) -> JsonResponse:
    return _get_order_details_for_role(request, order_id, 'waiter')


# ──────────────────────────────────────────────
# Waiter: Mesas y acciones
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
def waiter_tables(request):
    """Lista las mesas del establecimiento del camarero con estado actual."""
    establishment = _get_primary_establishment(request.user, 'waiter')
    if not establishment:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    tables = establishment.tables.filter(active=True).order_by('number')

    active_orders = Order.objects.filter(
        establishment=establishment,
        status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE],
        paid=False,
    ).annotate(items_count=Count('details'))

    active_orders_map = {order.table_id: order for order in active_orders}

    STATUS_MAP = {
        Order.Status.INITIATED: 'pending',
        Order.Status.IN_PROGRESS: 'in_progress',
        Order.Status.DONE: 'done',
    }

    tables_data = []
    for table in tables:
        active_order = active_orders_map.get(table.id)

        status = 'free'
        order_info = None

        if active_order:
            status = STATUS_MAP.get(active_order.status, 'free')

            order_info = {
                'id': active_order.id,
                'status': active_order.status,
                'status_display': active_order.get_status_display(),
                'total': f'{active_order.total:.2f}',
                'items_count': active_order.items_count,
                'placed_at': active_order.placed_at.isoformat(),
            }

        tables_data.append(
            {
                'number': table.number,
                'max_guests': table.max_guests,
                'status': status,
                'order': order_info,
            }
        )

    return JsonResponse(
        {
            'establishment': establishment.name,
            'tables': tables_data,
        }
    )


@require_http_methods('GET')
@auth_required
def waiter_table_order(request, table_num):
    """Ve el pedido activo de una mesa con todos sus detalles."""
    establishment = _get_primary_establishment(request.user, 'waiter')
    if not establishment:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    active_order = (
        Order.objects.filter(
            table__number=table_num,
            establishment=establishment,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE],
            paid=False,
        )
        .prefetch_related(
            Prefetch('details', queryset=OrderDetail.objects.select_related('product'))
        )
        .first()
    )

    if not active_order:
        if not establishment.tables.filter(number=table_num).exists():
            return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)
        return JsonResponse({'order': None})

    return JsonResponse(
        {
            'order': {
                'id': active_order.id,
                'status': active_order.status,
                'status_display': active_order.get_status_display(),
                'table_number': table_num,
                'placed_at': active_order.placed_at.isoformat(),
                'total': f'{active_order.total:.2f}',
                'paid': active_order.paid,
                'items': [
                    {
                        'id': d.id,
                        'product_name': d.product.name,
                        'price': f'{d.price:.2f}',
                        'quantity': d.quantity,
                        'notes': d.notes,
                    }
                    for d in active_order.details.all()
                ],
            }
        }
    )


@csrf_exempt
@require_http_methods('POST')
@auth_required
def waiter_advance_order(request, order_id):
    return _advance_order(request, order_id, 'waiter')


@csrf_exempt
@require_http_methods('POST')
@auth_required
def waiter_cancel_order(request, order_id):
    """Cancela un pedido activo."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    try:
        order = Order.objects.get(
            id=order_id,
            establishment_id__in=est_ids,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
        )
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Pedido no encontrado o ya cerrado.'}, status=404)

    order.status = Order.Status.CANCELLED
    order.closed_at = timezone.now()
    order.save()
    return JsonResponse({'message': 'Pedido cancelado.'})


@csrf_exempt
@require_http_methods('POST')
@auth_required
def waiter_close_table(request, table_num):
    """Cierra la mesa: marca el pedido como pagado."""
    establishment = _get_primary_establishment(request.user, 'waiter')
    if not establishment:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)

    active_order = _get_active_order_for_table(table, establishment)

    if not active_order:
        return JsonResponse({'error': 'No hay pedido activo en esta mesa.'}, status=400)

    active_order.paid = True
    active_order.status = Order.Status.DONE
    active_order.closed_at = timezone.now()
    active_order.save()

    return JsonResponse(
        {
            'message': f'Mesa {table.number} cerrada. Total: {active_order.total:.2f}€',
            'total': f'{active_order.total:.2f}',
        }
    )


# ──────────────────────────────────────────────
# Kitchen: Pedidos activos y acciones
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
def kitchen_active_orders(request):
    establishment = _get_primary_establishment(request.user, 'kitchen')
    if not establishment:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    orders = (
        Order.objects.filter(
            establishment=establishment,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
        )
        .select_related('table')
        .prefetch_related('details__product')
        .order_by('placed_at')
    )

    orders_data = []
    for order in orders:
        items = order.details.all()
        ready_count = items.filter(ready=True).count()
        total_count = items.count()

        orders_data.append(
            {
                'id': order.id,
                'status': order.status,
                'status_display': order.get_status_display(),
                'table_number': order.table.number,
                'placed_at': order.placed_at.isoformat(),
                'total': f'{order.total:.2f}',
                'ready_count': ready_count,
                'total_count': total_count,
                'items': [
                    {
                        'id': d.id,
                        'product_name': d.product.name,
                        'quantity': d.quantity,
                        'notes': d.notes,
                        'ready': d.ready,
                    }
                    for d in items
                ],
            }
        )

    return JsonResponse(
        {
            'establishment': establishment.name,
            'orders': orders_data,
        }
    )


@csrf_exempt
@require_http_methods('POST')
@auth_required
def kitchen_advance_order(request, order_id):
    return _advance_order(request, order_id, 'kitchen')


@csrf_exempt
@require_http_methods('POST')
@auth_required
def kitchen_toggle_item(request, item_id):
    """Marca o desmarca un plato individual como listo."""
    est_ids = _get_est_ids_by_role(request.user, 'kitchen')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    try:
        item = OrderDetail.objects.select_related('order').get(
            id=item_id,
            order__establishment_id__in=est_ids,
            order__status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
        )
    except OrderDetail.DoesNotExist:
        return JsonResponse({'error': 'Plato no encontrado.'}, status=404)

    item.ready = not item.ready
    item.save()

    order = item.order

    if order.status == Order.Status.INITIATED:
        order.status = Order.Status.IN_PROGRESS
        order.save()

    all_ready = not order.details.filter(ready=False).exists()
    if all_ready:
        order.status = Order.Status.DONE
        order.closed_at = timezone.now()
        order.save()

    return JsonResponse(
        {
            'message': f'{"Listo" if item.ready else "Pendiente"}: {item.product.name}',
            'item_ready': item.ready,
            'order_status': order.status,
            'order_done': all_ready,
        }
    )


@csrf_exempt
@require_http_methods('POST')
@auth_required
def kitchen_complete_order(request, order_id):
    """Marca TODOS los platos de un pedido como listos de una vez (batch)."""
    est_ids = _get_est_ids_by_role(request.user, 'kitchen')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    try:
        order = Order.objects.get(
            id=order_id,
            establishment_id__in=est_ids,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
        )
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Pedido no encontrado.'}, status=404)

    order.details.filter(ready=False).update(ready=True)
    order.status = Order.Status.DONE
    order.closed_at = timezone.now()
    order.save()

    return JsonResponse(
        {
            'message': f'Pedido #{order.id} completado.',
            'order_done': True,
        }
    )


# ──────────────────────────────────────────────
# Público: Crear pedido desde QR
# ──────────────────────────────────────────────


@csrf_exempt
@require_http_methods('POST')
@parse_json
@transaction.atomic
def create_public_order(request, establishment_cif):
    try:
        establishment = Establishment.objects.get(cif=establishment_cif)
    except Establishment.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento no encontrado'}, status=404)

    table_num = request.payload.get('table')
    items = request.payload.get('items', [])

    if not table_num or not items:
        return JsonResponse({'error': 'Mesa e items son obligatorios'}, status=400)

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Mesa no encontrada'}, status=404)

    # Validamos todos los productos antes de crear nada
    order_items = []
    invalid_ids = []
    total = 0

    for item in items:
        product_id = item.get('product_id')
        try:
            product = establishment.products.get(pk=product_id, available=True)
            quantity = item.get('quantity', 1)
            notes = item.get('notes', '')
            total += product.price * quantity
            order_items.append(
                {
                    'product': product,
                    'quantity': quantity,
                    'price': product.price,
                    'notes': notes,
                }
            )
        except Product.DoesNotExist:
            invalid_ids.append(product_id)

    if not order_items:
        return JsonResponse({'error': 'Ningún producto válido en el pedido'}, status=400)

    order = Order.objects.create(
        establishment=establishment,
        table=table,
        total=total,
    )

    OrderDetail.objects.bulk_create(
        [
            OrderDetail(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                notes=item['notes'],
            )
            for item in order_items
        ]
    )

    response = {'ok': True, 'order_id': order.pk}
    if invalid_ids:
        response['skipped_product_ids'] = invalid_ids

    return JsonResponse(response, status=201)
