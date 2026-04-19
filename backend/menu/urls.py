from django.urls import path

from . import views

urlpatterns = [
    path('<str:establishment_cif>/tables/', views.public_tables, name='public-tables'),
    path('<str:establishment_cif>/products/', views.public_products, name='public-products'),
]
