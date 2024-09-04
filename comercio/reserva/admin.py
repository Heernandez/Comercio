from django.contrib import admin
from .models import Reserva, ProductoReserva

class ProductoReservaInline(admin.TabularInline):
    model = ProductoReserva
    extra = 1  # Número de líneas adicionales en blanco que se muestran

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estado', 'cantidad_total', 'valor_total', 'fecha_reserva')
    actions = ['aceptar_reservas', 'rechazar_reservas']
    inlines = [ProductoReservaInline]  # Asocia ProductoReserva con Reserva en el admin

    def aceptar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.aceptar()
    aceptar_reservas.short_description = "Aceptar reservas seleccionadas"

    def rechazar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.rechazar()
    rechazar_reservas.short_description = "Rechazar reservas seleccionadas"

admin.site.register(Reserva, ReservaAdmin)
