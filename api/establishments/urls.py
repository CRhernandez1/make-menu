from django.urls import include, path

from . import views

app_name = 'establishments'

urlpatterns = [
    path('', views.establishments_list, name='establishment-list'),
    path('<str:establishment_cif>/tables/', views.tables_list, name='create-table'),
    path('<str:establishment_cif>/tables/add/', views.add_table, name='add-table'),
    path(
        '<str:establishment_cif>/tables/<int:table_num>/',
        views.table_detail,
        name='table-detail',
    ),
    path(
        '<str:establishment_cif>/tables/<int:table_num>/edit/',
        views.edit_table,
        name='edit-table',
    ),
    path(
        '<str:establishment_cif>/tables/<int:table_num>/delete/',
        views.delete_table,
        name='delete-table',
    ),
    path(
        '<str:establishment_cif>/tables/<int:table_num>/change/',
        views.change_table_status,
        name='change-table-status',
    ),
    path('<str:establishment_cif>/products/', include('products.urls')),
]
