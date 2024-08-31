# nombre_de_la_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta para la vista 'index'
    path('detalle/', views.detalle, name='detalle'),  # Otra ruta como ejemplo
]
