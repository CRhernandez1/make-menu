from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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


@require_http_methods(['GET'])
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


@require_http_methods(['GET'])
@auth_required
def get_order_details(request, order_id: int) -> JsonResponse:
    """Devuelve los detalles (los platos y notas) asociados a un ticket de pedido específico."""
    est_ids = _get_est_ids_by_role(request.user, 'manager')
    order = get_object_or_404(Order, pk=order_id, establishment_id__in=est_ids)

    order_details = order.details.select_related('product')
    return OrderDetailSerializer(order_details, request=request).json_response()


@require_http_methods(['GET'])
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


@require_http_methods(['GET'])
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
