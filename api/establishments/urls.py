from django.urls import path

from . import views

app_name = 'establishments'

urlpatterns = [path('', views.establishments_list, name='establishment-list')]
