from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from historial.models import Historial  # Importa el modelo Historial
from django.conf import settings
from producto.models import Producto, Subproducto 

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    
    codigo_reserva = models.CharField(max_length=100, unique=True, editable=False)  # ID de reserva personalizado
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #productos = models.TextField()  # Aquí podrías almacenar un JSON con los IDs y cantidades de productos/subproductos.
    cantidad_total = models.PositiveIntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_reserva = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.username} - {self.estado}"

    def aceptar(self):
        self.estado = 'aceptado'
        self.save()
        Historial.crear_desde_reserva(self)

    def rechazar(self):
        self.estado = 'rechazado'
        self.devolver_stock()
        self.save()
        Historial.crear_desde_reserva(self)

    def devolver_stock(self):
        # Implementar lógica para devolver la cantidad de productos al stock original
        # Podrías parsear el campo `productos` y actualizar el stock de cada producto
        pass

class ProductoReserva(models.Model):
    reserva = models.ForeignKey(Reserva, related_name='productos_reserva', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    subproducto = models.ForeignKey(Subproducto, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField()

    def __str__(self):
        if self.subproducto:
            return f"Producto: {self.producto.nombre} (Subproducto: {self.subproducto.nombre}) en Reserva {self.reserva.codigo_reserva}"
        return f"Producto: {self.producto.nombre} en Reserva {self.reserva.codigo_reserva}"