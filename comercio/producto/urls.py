# nombre_de_la_app/urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('detalle/', views.detalle, name='detalle'),  # Otra ruta como ejemplo
    path('', views.productos, name='productos'),
    path('<int:id>/', views.producto_detalle, name='producto_detalle'),
    path('api/actualizar-stock/',  views.actualizar_stock, name='actualizar_stock'),
]
