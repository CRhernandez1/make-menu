from django.http import JsonResponse

from establishments.models import Establishment
from establishments.serializers import TableSerializer
from products.serializers import ProductSerializer
from shared.decorators import require_http_methods


@require_http_methods('GET')
def public_tables(request, establishment_cif):
    try:
        establishment = Establishment.objects.get(cif=establishment_cif)
    except Establishment.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento no encontrado'}, status=404)

    tables = establishment.tables.filter(active=True)
    return TableSerializer(tables).json_response()


@require_http_methods('GET')
def public_products(request, establishment_cif):
    try:
        establishment = Establishment.objects.get(cif=establishment_cif)
    except Establishment.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento no encontrado'}, status=404)

    products = establishment.products.filter(available=True)
    return ProductSerializer(products).json_response()
