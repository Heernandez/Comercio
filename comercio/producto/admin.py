# producto/admin.py

from django.contrib import admin
from .models import Producto, Variante, Imagen

class ImagenInline(admin.TabularInline):
    model = Producto.imagenes.through
    extra = 1
    verbose_name = "Imagen"
    verbose_name_plural = "Imágenes para Producto"

class VarianteInline(admin.TabularInline):
    model = Variante
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'descripcion')
    inlines = [VarianteInline]
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para el producto

class VarianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'producto', 'stock_disponible', 'precio')
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para la variante

class ImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagen')
    readonly_fields = ('imagen',)  # Opcional: marca el campo de imagen como solo lectura

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variante, VarianteAdmin)
admin.site.register(Imagen, ImagenAdmin)
