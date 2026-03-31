from django.urls import path

from . import views

urlpatterns = [
    path('invite/', views.generate_invitation, name='generate-invitation'),
]
