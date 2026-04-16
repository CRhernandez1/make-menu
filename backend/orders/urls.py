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
    path('waiter-orders/', views.list_waiter_orders, name='waiter-orders-list'),
    path(
        'waiter-orders/<int:order_id>/details/',
        views.get_waiter_order_details,
        name='waiter-order-details',
    ),
]
