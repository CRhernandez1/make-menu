from datetime import timedelta

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


def _get_est_ids_by_role(user, role):
    """Devuelve una lista plana con los IDs de establecimientos donde el usuario ejerce el rol indicado."""
    return list(
        user.manages.filter(role=role, end_date__isnull=True).values_list(
            'establishment_id', flat=True
        )
    )


@require_http_methods('GET')
@auth_required
def list_manager_orders(request) -> JsonResponse:
    """Extrae y filtra los pedidos del manager en base a tiempo y local específico."""
    est_ids = _get_est_ids_by_role(request.user, 'manager')
    if not est_ids:
        return JsonResponse([], safe=False)

    queryset = Order.objects.filter(establishment_id__in=est_ids).select_related(
        'table', 'establishment'
    )

    est_id = request.GET.get('establishment_id')
    if est_id and est_id.isdigit() and int(est_id) in est_ids:
        queryset = queryset.filter(establishment_id=est_id)

    days = request.GET.get('days')
    if days and days.isdigit():
        time_threshold = timezone.now() - timedelta(days=int(days))
        queryset = queryset.filter(placed_at__gte=time_threshold)

    orders_sorted = queryset.order_by('-placed_at')
    return OrderSerializer(orders_sorted, request=request).json_response()


@require_http_methods('GET')
@auth_required
def get_order_details(request, order_id: int) -> JsonResponse:
    """Devuelve los detalles (los platos y notas) asociados a un ticket de pedido específico."""
    est_ids = _get_est_ids_by_role(request.user, 'manager')
    order = get_object_or_404(Order, pk=order_id, establishment_id__in=est_ids)

    order_details = order.details.select_related('product')
    return OrderDetailSerializer(order_details, request=request).json_response()


@require_http_methods('GET')
@auth_required
def list_waiter_orders(request) -> JsonResponse:
    """Extrae y filtra los pedidos del camarero en base a tiempo y local específico."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    if not est_ids:
        return JsonResponse([], safe=False)

    queryset = Order.objects.filter(establishment_id__in=est_ids).select_related(
        'table', 'establishment'
    )

    est_id = request.GET.get('establishment_id')
    if est_id and est_id.isdigit() and int(est_id) in est_ids:
        queryset = queryset.filter(establishment_id=est_id)

    days = request.GET.get('days')
    if days and days.isdigit():
        time_threshold = timezone.now() - timedelta(days=int(days))
        queryset = queryset.filter(placed_at__gte=time_threshold)

    orders_sorted = queryset.order_by('-placed_at')
    return OrderSerializer(orders_sorted, request=request).json_response()


@csrf_exempt
@require_http_methods('GET')
@auth_required
def get_waiter_order_details(request, order_id: int) -> JsonResponse:
    """Devuelve los detalles asociados a un ticket de pedido para un camarero."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    order = get_object_or_404(Order, pk=order_id, establishment_id__in=est_ids)

    order_details = order.details.select_related('product')
    return OrderDetailSerializer(order_details, request=request).json_response()


@csrf_exempt
@require_http_methods('POST')
@parse_json
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

    # Validamos y calculamos el total antes de crear el pedido
    order_items = []
    total = 0

    for item in items:
        try:
            product = establishment.products.get(pk=item['product_id'], available=True)
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
            continue

    if not order_items:
        return JsonResponse({'error': 'Ningún producto válido en el pedido'}, status=400)

    order = Order.objects.create(
        establishment=establishment,
        table=table,
        total=total,
    )

    for item in order_items:
        OrderDetail.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
            notes=item['notes'],
        )

    return JsonResponse({'ok': True, 'order_id': order.pk}, status=201)
# ──────────────────────────────────────────────
# Waiter: Mesas y acciones
# ──────────────────────────────────────────────

@require_http_methods('GET')
@auth_required
def waiter_tables(request):
    """Lista las mesas del establecimiento del camarero con estado actual."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    establishment = Establishment.objects.get(pk=est_ids[0])
    tables = establishment.tables.filter(active=True).order_by('number')

    tables_data = []
    for table in tables:
        active_order = Order.objects.filter(
            table=table,
            establishment=establishment,
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE]
        ).exclude(paid=True).first()

        status = 'free'
        order_info = None

        if active_order:
            if active_order.status == Order.Status.INITIATED:
                status = 'pending'
            elif active_order.status == Order.Status.IN_PROGRESS:
                status = 'in_progress'
            elif active_order.status == Order.Status.DONE:
                status = 'done'

            order_info = {
                'id': active_order.id,
                'status': active_order.status,
                'status_display': active_order.get_status_display(),
                'total': f'{active_order.total:.2f}',
                'items_count': active_order.details.count(),
                'placed_at': active_order.placed_at.isoformat(),
            }

        tables_data.append({
            'number': table.number,
            'max_guests': table.max_guests,
            'status': status,
            'order': order_info,
        })

    return JsonResponse({
        'establishment': establishment.name,
        'tables': tables_data,
    })


@require_http_methods('GET')
@auth_required
def waiter_table_order(request, table_num):
    """Ve el pedido activo de una mesa con todos sus detalles."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    establishment = Establishment.objects.get(pk=est_ids[0])

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)

    active_order = Order.objects.filter(
        table=table,
        establishment=establishment,
        status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE]
    ).exclude(paid=True).first()

    if not active_order:
        return JsonResponse({'order': None})

    details = active_order.details.select_related('product').all()

    return JsonResponse({
        'order': {
            'id': active_order.id,
            'status': active_order.status,
            'status_display': active_order.get_status_display(),
            'table_number': table.number,
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
                for d in details
            ],
        }
    })


@csrf_exempt
@require_http_methods('POST')
@auth_required
def waiter_advance_order(request, order_id):
    """Avanza el estado: INITIATED -> IN_PROGRESS -> DONE."""
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
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
    return JsonResponse({
        'message': f'Pedido actualizado a "{order.get_status_display()}".',
        'status': order.status,
        'status_display': order.get_status_display(),
    })


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
            status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS]
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
    est_ids = _get_est_ids_by_role(request.user, 'waiter')
    if not est_ids:
        return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)

    establishment = Establishment.objects.get(pk=est_ids[0])

    try:
        table = establishment.tables.get(number=table_num)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)

    active_order = Order.objects.filter(
        table=table,
        establishment=establishment,
        status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE]
    ).exclude(paid=True).first()

    if not active_order:
        return JsonResponse({'error': 'No hay pedido activo en esta mesa.'}, status=400)

    active_order.paid = True
    active_order.status = Order.Status.DONE
    active_order.closed_at = timezone.now()
    active_order.save()

    return JsonResponse({
        'message': f'Mesa {table.number} cerrada. Total: {active_order.total:.2f}€',
        'total': f'{active_order.total:.2f}',
    })


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
            order__status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS]
        )
    except OrderDetail.DoesNotExist:
        return JsonResponse({'error': 'Plato no encontrado.'}, status=404)

    # Toggle ready
    item.ready = not item.ready
    item.save()

    order = item.order

    # Si el pedido estaba INITIATED y se marca algo, pasa a IN_PROGRESS
    if order.status == Order.Status.INITIATED:
        order.status = Order.Status.IN_PROGRESS
        order.save()

    # Si todos los platos están listos, el pedido pasa a DONE
    all_ready = not order.details.filter(ready=False).exists()
    if all_ready:
        order.status = Order.Status.DONE
        order.closed_at = timezone.now()
        order.save()

    return JsonResponse({
        'message': f'{"Listo" if item.ready else "Pendiente"}: {item.product.name}',
        'item_ready': item.ready,
        'order_status': order.status,
        'order_done': all_ready,
    })

