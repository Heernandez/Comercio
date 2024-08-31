# nombre_de_la_app/admin.py

from django.contrib import admin
from .models import Producto,Imagen

# Registra el modelo en el sitio de administración
admin.site.register(Producto)
admin.site.register(Imagen)
