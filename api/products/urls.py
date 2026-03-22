from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    # products
    path('', views.products_list, name='product-list'),
    path('add/', views.add_product, name='product-add'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('<int:product_id>/delete/', views.delete_product, name='product-delete'),
    path('<int:product_id>/edit/', views.edit_product, name='product-edit'),
    # ingredients
    path('ingredients/', views.ingredients_list, name='ingredients-list'),
    path('ingredients/add/', views.add_ingredient, name='ingredient-add'),
    path('ingredients/<int:ingredient_id>/', views.ingredient_detail, name='ingredient-detail'),
    path(
        'ingredients/<int:ingredient_id>/delete', views.delete_ingredient, name='ingredient-delete'
    ),
    path('ingredients/<int:ingredient_id>/edit', views.edit_ingredient, name='ingredient-edit'),
]
