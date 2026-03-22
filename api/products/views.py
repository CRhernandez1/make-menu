from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from establishments.models import Establishment
from shared.decorators import get_instance_or_404, parse_json_to_python, require_http_methods

from .models import Category, Product
from .serializers import ProductSerializer


@get_instance_or_404(Establishment, 'cif', 'Establishment')
def products_list(request, establishment_cif):
    establishment = request.instance
    products = establishment.products.all()
    return ProductSerializer(products).json_response()


@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def product_detail(request, establishment_cif, product_id):
    establishment = request.instance
    try:
        product = establishment.products.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)
    return ProductSerializer(product).json_response()


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python('name', 'description', 'price', 'category')
def add_product(request, establishment_cif):
    establishment = request.instance
    payload = request.payload
    category = Category.objects.get(id=payload['category'])

    name = payload['name']
    description = payload['description']
    price = payload['price']

    product = Product.objects.create(
        establishment=establishment,
        name=name,
        description=description,
        price=price,
        category=category,
    )
    return JsonResponse({'id': product.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def delete_product(request, establishment_cif, product_id):
    establishment = request.instance

    try:
        product = establishment.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    product.delete()
    return JsonResponse({'message': 'Product delete succesfully'}, status=204)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python()
def edit_product(request, establishment_cif, product_id):
    establishment = request.instance
    payload = request.payload
    try:
        product = establishment.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    ### por si no se actualizan todos los campos desde el frontend, ejemplo actualizan nombre pero no descripcion.
    if 'category' in payload:
        try:
            category = Category.objects.get(id=payload['category'])
            product.category = category
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)

    if 'name' in payload:
        product.name = payload['name']
    if 'description' in payload:
        product.description = payload['description']
    if 'price' in payload:
        product.price = payload['price']

    product.save()
    return JsonResponse({'message': 'Product updated!'}, status=200)
