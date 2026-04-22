from django.urls import path
from . import views

urlpatterns = [
    # Manager
    path('manager-orders/', views.list_manager_orders, name='manager-orders-list'),
    path('manager-orders/<int:order_id>/details/', views.get_order_details, name='manager-order-details'),

    # Waiter - listado
    path('waiter-orders/', views.list_waiter_orders, name='waiter-orders-list'),
    path('waiter-orders/<int:order_id>/details/', views.get_waiter_order_details, name='waiter-order-details'),

    # Waiter - mesas y acciones
    path('waiter/tables/', views.waiter_tables, name='waiter-tables'),
    path('waiter/tables/<int:table_num>/order/', views.waiter_table_order, name='waiter-table-order'),
    path('waiter/tables/<int:table_num>/close/', views.waiter_close_table, name='waiter-close-table'),
    path('waiter/orders/<int:order_id>/advance/', views.waiter_advance_order, name='waiter-advance-order'),
    path('waiter/orders/<int:order_id>/cancel/', views.waiter_cancel_order, name='waiter-cancel-order'),

    # Kitchen
    path('kitchen/orders/', views.kitchen_active_orders, name='kitchen-active-orders'),
    path('kitchen/orders/<int:order_id>/advance/', views.kitchen_advance_order, name='kitchen-advance-order'),
    path('kitchen/items/<int:item_id>/toggle/', views.kitchen_toggle_item, name='kitchen-toggle-item'),

    # Público
    path('public/<str:establishment_cif>/', views.create_public_order, name='public-order-create'),
]