from django.contrib import admin
from django.conf import settings
from .models import Producto, Subproducto, Imagen

class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1

class SubproductoInline(admin.StackedInline):  # O TabularInline según tu preferencia
    model = Subproducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'descripcion', 'creado_por')
    inlines = [SubproductoInline]  # Permite gestionar subproductos desde la página del producto
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para el producto
    readonly_fields = ('creado_por',)  # Haz que el campo 'creado_por' sea de solo lectura en el admin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filtra los productos para que el usuario solo vea los que ha creado
            qs = qs.filter(creado_por=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            # Si el objeto es nuevo, asigna el usuario actual como creador
            obj.creado_por = request.user
        obj.save()

@admin.register(Subproducto)
class SubproductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'producto', 'precio')
    filter_horizontal = ('imagenes',)  # Permite seleccionar múltiples imágenes para el subproducto

admin.site.register(Imagen)
