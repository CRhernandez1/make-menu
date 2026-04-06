from django.urls import include, path

from . import views

urlpatterns = [
    path('invite/', views.generate_invitation, name='generate-invitation'),
    path(
        'invite/validate/<str:invitation_id>/',
        views.validate_invitation,
        name='validate-invitation',
    ),
    path('<str:establishment_cif>/products/', include('products.urls')),
]
