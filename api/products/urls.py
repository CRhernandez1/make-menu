from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='product-list'),
    path('add/', views.add_product, name='product-add'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('<int:product_id>/delete/', views.delete_product, name='product-delete'),
    path('<int:product_id>/edit/', views.edit_product, name='product-edit'),
]
