from django.contrib import admin
from .models import Historial

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estado', 'fecha_reserva', 'fecha_historial')
    search_fields = ('usuario__username', 'estado')
    list_filter = ('estado', 'fecha_historial')
    readonly_fields = ('usuario', 'productos', 'cantidad_total', 'valor_total', 'estado', 'fecha_reserva', 'fecha_historial')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
