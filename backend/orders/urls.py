# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('manager-orders/', views.list_manager_orders, name='manager-orders-list'),
    path(
        'manager-orders/<int:order_id>/details/',
        views.get_order_details,
        name='manager-order-details',
    ),
]
