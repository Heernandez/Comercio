from django.db import models
import os
from django.conf import settings

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return os.path.basename(self.imagen.name)

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    contacto_de_referencia = models.CharField(max_length=255)
    stock_disponible = models.IntegerField(default=0)
    imagenes = models.ManyToManyField(Imagen, blank=True, related_name='productos')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def stock_total(self):
        total_stock_subproductos = sum(subproducto.stock_disponible for subproducto in self.subproductos.all())
        return self.stock_disponible + total_stock_subproductos

    def __str__(self):
        return self.nombre

class Subproducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='subproductos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.IntegerField(default=0)
    imagenes = models.ManyToManyField(Imagen, blank=True, related_name='subproductos')

    def __str__(self):
        return self.nombre
