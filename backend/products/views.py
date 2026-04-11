from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from establishments.models import Establishment
from shared.decorators import get_instance_or_404, parse_json_to_python, require_http_methods

from .models import Allergen, Category, Component, Ingredient, Product
from .serializers import (
    AllergenSerializer,
    CategorySerializer,
    IngredientSerializer,
    ProductSerializer,
)

# Ingredient, Allergen


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


@get_instance_or_404(Establishment, 'cif', 'Establishment')
def ingredients_list(request, establishment_cif):
    establishment = request.instance
    ingredients = establishment.ingredients.all()
    return IngredientSerializer(ingredients).json_response()


@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def ingredient_detail(request, establishment_cif, ingredient_id):
    establishment = request.instance
    try:
        ingredient = establishment.ingredients.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)
    return IngredientSerializer(ingredient).json_response()


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python('name', 'ingredient_type')
def add_ingredient(request, establishment_cif):
    establishment = request.instance
    payload = request.payload

    ingredient = Ingredient.objects.create(
        establishment=establishment,
        name=payload['name'],
        ingredient_type=payload['ingredient_type'],
        description=payload.get('description', ''),
        available=payload.get('available', True),
    )

    # ManyToMany se asigna después de crear
    if 'allergens' in payload:
        ingredient.allergens.set(payload['allergens'])

    return JsonResponse({'id': ingredient.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def delete_ingredient(request, establishment_cif, ingredient_id):
    establishment = request.instance

    try:
        ingredient = establishment.ingredients.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)

    ingredient.delete()
    return JsonResponse({'message': 'Ingredient delete succesfully'}, status=204)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python()
def edit_ingredient(request, establishment_cif, ingredient_id):
    establishment = request.instance
    payload = request.payload
    try:
        ingredient = establishment.ingredients.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)

    ### por si no se actualizan todos los campos desde el frontend, ejemplo actualizan nombre pero no descripcion.

    if 'ingredient_type' in payload:
        ingredient.ingredient_type = payload['ingredient_type']

    if 'name' in payload:
        ingredient.name = payload['name']

    if 'description' in payload:
        ingredient.description = payload['description']

    if 'allergens' in payload:
        ingredient.allergens.set(payload['allergens'])

    ingredient.save()
    return JsonResponse({'message': 'Ingredient updated!'}, status=200)


@get_instance_or_404(Establishment, 'cif', 'Establishment')
def categories_list(request, establishment_cif):
    establishment = request.instance
    categories = establishment.categories.all()
    return CategorySerializer(categories).json_response()


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python('name')
def add_category(request, establishment_cif):
    establishment = request.instance
    payload = request.payload

    category = Category.objects.create(establishment=establishment, name=payload['name'])

    return JsonResponse({'id': category.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def delete_category(request, establishment_cif, category_id):
    establishment = request.instance

    try:
        category = establishment.categories.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found!'}, status=404)

    category.delete()
    return JsonResponse({'message': 'Category delete succesfully'}, status=204)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python()
def edit_category(request, establishment_cif, category_id):
    establishment = request.instance
    payload = request.payload
    try:
        category = establishment.categories.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found!'}, status=404)

    if 'name' in payload:
        category.name = payload['name']

    category.save()
    return JsonResponse({'message': 'Category updated!'}, status=200)


@require_http_methods('GET')
def allergens_list(request):
    allergens = Allergen.objects.all()
    return AllergenSerializer(allergens).json_response()


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def upload_product_image(request, establishment_cif, product_id):
    establishment = request.instance
    try:
        product = establishment.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    image = request.FILES.get('product_image')
    if not image:
        return JsonResponse({'error': 'No image provided'}, status=400)

    product.product_image = image
    product.save()
    return JsonResponse({'product_image': product.product_image.url}, status=200)


@require_http_methods('GET')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def components_list(request, establishment_cif, product_id):
    establishment = request.instance
    product = establishment.products.get(pk=product_id)
    components = product.components.select_related('ingredient').all()
    return JsonResponse(
        [
            {
                'id': c.id,
                'ingredient': c.ingredient.id,
                'ingredient_name': c.ingredient.name,
                'quantity': str(c.quantity),
                'unity': c.unity,
                'removable': c.removable,
            }
            for c in components
        ],
        safe=False,
    )


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@parse_json_to_python('ingredient', 'quantity', 'unity')
def add_component(request, establishment_cif, product_id):
    establishment = request.instance
    payload = request.payload
    product = establishment.products.get(pk=product_id)
    ingredient = establishment.ingredients.get(pk=payload['ingredient'])
    component = Component.objects.create(
        product=product,
        ingredient=ingredient,
        quantity=payload['quantity'],
        unity=payload['unity'],
        removable=payload.get('removable', False),
    )
    return JsonResponse({'id': component.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@get_instance_or_404(Establishment, 'cif', 'Establishment')
def delete_component(request, establishment_cif, product_id, component_id):
    establishment = request.instance
    product = establishment.products.get(pk=product_id)
    component = product.components.get(pk=component_id)
    component.delete()
    return JsonResponse({'message': 'Component deleted'}, status=200)
