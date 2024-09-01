from django.contrib import admin
from .models import Producto, Subproducto, Imagen

class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1

class SubproductoInline(admin.StackedInline):  # O TabularInline según tu preferencia
    model = Subproducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'descripcion')
    inlines = [SubproductoInline]  # Permite gestionar subproductos desde la página del producto
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para el producto

@admin.register(Subproducto)
class SubproductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'producto', 'precio')
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para el subproducto

admin.site.register(Imagen)
