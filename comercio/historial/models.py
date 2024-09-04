from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Historial(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productos = models.TextField()
    cantidad_total = models.PositiveIntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10)
    fecha_reserva = models.DateTimeField()
    fecha_historial = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Historial {self.id} - {self.usuario.username} - {self.estado}"

    @classmethod
    def crear_desde_reserva(cls, reserva):
        cls.objects.create(
            usuario=reserva.usuario,
            productos=reserva.productos,
            cantidad_total=reserva.cantidad_total,
            valor_total=reserva.valor_total,
            estado=reserva.estado,
            fecha_reserva=reserva.fecha_reserva
        )
        reserva.delete()
