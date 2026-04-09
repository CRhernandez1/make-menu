from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from users.decorators import auth_required

from .models import Order
from .serializers import OrderDetailSerializer, OrderSerializer


# --- HELPER (Función auxiliar) ---
def _get_manager_est_ids(user):
    """Devuelve los IDs de los establecimientos que el usuario gestiona actualmente."""
    # CORRECCIÓN: Quitamos '.member' porque la relación 'manages' apunta directo al User
    return user.manages.filter(role='manager', end_date__isnull=True).values_list(
        'establishment_id', flat=True
    )


@require_http_methods(['GET'])
@auth_required
def list_manager_orders(request):
    # 1. Seguridad: Obtener IDs permitidos
    est_ids = _get_manager_est_ids(request.user)
    if not est_ids:
        return JsonResponse([], safe=False)

    # 2. Queryset base
    queryset = Order.objects.filter(establishment_id__in=est_ids).select_related(
        'table', 'establishment'
    )

    # 3. Filtros en una sola línea usando .isdigit() para evitar try/except
    est_id = request.GET.get('establishment_id')
    if est_id and est_id.isdigit() and int(est_id) in est_ids:
        queryset = queryset.filter(establishment_id=est_id)

    days = request.GET.get('days')
    if days and days.isdigit():
        time_threshold = timezone.now() - timedelta(days=int(days))
        queryset = queryset.filter(placed_at__gte=time_threshold)

    # 4. Respuesta (Añadimos el order_by al final)
    return OrderSerializer(queryset.order_by('-placed_at'), request=request).json_response()


@require_http_methods(['GET'])
@auth_required
def get_order_details(request, order_id):
    # 1. Seguridad y obtención del pedido en dos líneas
    est_ids = _get_manager_est_ids(request.user)
    order = get_object_or_404(Order, pk=order_id, establishment_id__in=est_ids)

    # 2. Respuesta serializada
    return OrderDetailSerializer(
        order.details.select_related('product'), request=request
    ).json_response()
