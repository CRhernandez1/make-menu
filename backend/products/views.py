from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from establishments.models import Establishment, Manage
from shared.decorators import get_instance_or_404, parse_json, require_http_methods, require_role
from users.decorators import auth_required

from .forms import (
    CategoryForm,
    ComponentCreateForm,
    IngredientCreateForm,
    IngredientUpdateForm,
    ProductCreateForm,
    ProductUpdateForm,
)
from .models import Allergen, Category, Component, Ingredient, Product
from .serializers import (
    AllergenSerializer,
    CategorySerializer,
    IngredientSerializer,
    ProductSerializer,
)

# ──────────────────────────────────────────────
# Products
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def products_list(request, establishment_cif):
    products = request.instance.products.all()
    return ProductSerializer(products, request=request).json_response()


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def product_detail(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)
    return ProductSerializer(product, request=request).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_product(request, establishment_cif):
    form = ProductCreateForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    product = form.save(commit=False)
    product.establishment = request.instance
    product.save()
    return JsonResponse({'id': product.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_product(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    form = ProductUpdateForm(request.payload, instance=product)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()
    return JsonResponse({'message': 'Product updated!'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_product(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    product.components.all().delete()
    product.delete()
    return JsonResponse({'message': 'Product deleted successfully.'}, status=204)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def upload_product_image(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    image = request.FILES.get('product_image')
    if not image:
        return JsonResponse({'error': 'No image provided'}, status=400)

    product.product_image = image
    product.save()
    return JsonResponse(
        {'product_image': request.build_absolute_uri(product.product_image.url)}, status=200
    )


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def toggle_product_available(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    product.available = not product.available
    product.save()
    return ProductSerializer(product, request=request).json_response()


# ──────────────────────────────────────────────
# Ingredients
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def ingredients_list(request, establishment_cif):
    ingredients = request.instance.ingredients.all()
    return IngredientSerializer(ingredients).json_response()


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def ingredient_detail(request, establishment_cif, ingredient_id):
    try:
        ingredient = request.instance.ingredients.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)
    return IngredientSerializer(ingredient).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_ingredient(request, establishment_cif):
    form = IngredientCreateForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    ingredient = form.save(commit=False)
    ingredient.establishment = request.instance
    ingredient.save()

    if 'allergens' in request.payload:
        ingredient.allergens.set(request.payload['allergens'])

    return JsonResponse({'id': ingredient.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_ingredient(request, establishment_cif, ingredient_id):
    try:
        ingredient = request.instance.ingredients.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)

    form = IngredientUpdateForm(request.payload, instance=ingredient)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()

    if 'allergens' in request.payload:
        ingredient.allergens.set(request.payload['allergens'])

    return JsonResponse({'message': 'Ingredient updated!'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_ingredient(request, establishment_cif, ingredient_id):
    try:
        ingredient = request.instance.ingredients.get(pk=ingredient_id)
    except Ingredient.DoesNotExist:
        return JsonResponse({'message': 'Ingredient not found!'}, status=404)

    ingredient.delete()
    return JsonResponse({'message': 'Ingredient deleted successfully.'}, status=204)


# ──────────────────────────────────────────────
# Categories
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def categories_list(request, establishment_cif):
    categories = request.instance.categories.all()
    return CategorySerializer(categories).json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_category(request, establishment_cif):
    form = CategoryForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    category = form.save(commit=False)
    category.establishment = request.instance
    category.save()
    return JsonResponse({'id': category.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def edit_category(request, establishment_cif, category_id):
    try:
        category = request.instance.categories.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found!'}, status=404)

    form = CategoryForm(request.payload, instance=category)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    form.save()
    return JsonResponse({'message': 'Category updated!'}, status=200)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_category(request, establishment_cif, category_id):
    try:
        category = request.instance.categories.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found!'}, status=404)

    category.delete()
    return JsonResponse({'message': 'Category deleted successfully.'}, status=204)


# ──────────────────────────────────────────────
# Allergens
# ──────────────────────────────────────────────


@require_http_methods('GET')
def allergens_list(request):
    allergens = Allergen.objects.all()
    return AllergenSerializer(allergens).json_response()


# ──────────────────────────────────────────────
# Components
# ──────────────────────────────────────────────


@require_http_methods('GET')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role()
def components_list(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

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
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_component(request, establishment_cif, product_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    try:
        ingredient = request.instance.ingredients.get(pk=request.payload['ingredient'])
    except (Ingredient.DoesNotExist, KeyError):
        return JsonResponse({'message': 'Ingredient not found or missing!'}, status=400)

    form = ComponentCreateForm(request.payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    component = form.save(commit=False)
    component.product = product
    component.ingredient = ingredient
    component.save()
    return JsonResponse({'id': component.pk}, status=201)


@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
def delete_component(request, establishment_cif, product_id, component_id):
    try:
        product = request.instance.products.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found!'}, status=404)

    try:
        component = product.components.get(pk=component_id)
    except Component.DoesNotExist:
        return JsonResponse({'message': 'Component not found!'}, status=404)

    component.delete()
    return JsonResponse({'message': 'Component deleted successfully.'}, status=204)
