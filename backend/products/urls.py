from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    # products, categories and components
    path('', views.products_list, name='product-list'),
    path('add/', views.add_product, name='product-add'),
    path('categories/', views.categories_list, name='categories-list'),
    path('categories/add/', views.add_category, name='category-add'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='category-add'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='category-add'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('<int:product_id>/delete/', views.delete_product, name='product-delete'),
    path('<int:product_id>/edit/', views.edit_product, name='product-edit'),
    path('<int:product_id>/image/', views.upload_product_image, name='product-image'),
    path('<int:product_id>/components/', views.components_list, name='components-list'),
    path('<int:product_id>/components/add/', views.add_component, name='component-add'),
    path(
        '<int:product_id>/components/<int:component_id>/delete/',
        views.delete_component,
        name='component-delete',
    ),
    # ingredients
    path('ingredients/', views.ingredients_list, name='ingredients-list'),
    path('ingredients/add/', views.add_ingredient, name='ingredient-add'),
    path('ingredients/<int:ingredient_id>/', views.ingredient_detail, name='ingredient-detail'),
    path(
        'ingredients/<int:ingredient_id>/delete/', views.delete_ingredient, name='ingredient-delete'
    ),
    path('ingredients/<int:ingredient_id>/edit/', views.edit_ingredient, name='ingredient-edit'),
]
