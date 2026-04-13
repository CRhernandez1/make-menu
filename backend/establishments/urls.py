from django.urls import include, path
from . import views

urlpatterns = [
    # Establishments
    path('', views.establishments_list, name='establishment-list'),
    path('add/', views.add_establishment, name='add-establishment'),

    # Invitations
    path('invite/', views.generate_invitation, name='generate-invitation'),
    path('invite/validate/<str:invitation_id>/', views.validate_invitation, name='validate-invitation'),

    # Establishments CRUD
    path('<str:establishment_cif>/', views.establishment_detail, name='establishment-detail'),
    path('<str:establishment_cif>/edit/', views.edit_establishment, name='edit-establishment'),
    path('<str:establishment_cif>/delete/', views.delete_establishment, name='delete-establishment'),
    path('<str:establishment_cif>/toggle/', views.toggle_establishment, name='toggle-establishment'),

    # Products
    path('<str:establishment_cif>/products/', include('products.urls')),

    # Tables
    path('<str:establishment_cif>/tables/', views.tables_list, name='tables-list'),
    path('<str:establishment_cif>/tables/add/', views.add_table, name='add-table'),
    path('<str:establishment_cif>/tables/<int:table_num>/', views.table_detail, name='table-detail'),
    path('<str:establishment_cif>/tables/<int:table_num>/edit/', views.edit_table, name='edit-table'),
    path('<str:establishment_cif>/tables/<int:table_num>/delete/', views.delete_table, name='delete-table'),
    path('<str:establishment_cif>/tables/<int:table_num>/change/', views.change_table_status, name='change-table-status'),

    # Staff
    path('<str:establishment_cif>/staff/', views.staff_list, name='staff-list'),
    path('<str:establishment_cif>/staff/<int:member_id>/edit/', views.edit_staff, name='edit-staff'),
    path('<str:establishment_cif>/staff/<int:member_id>/remove/', views.remove_staff, name='remove-staff'),
]