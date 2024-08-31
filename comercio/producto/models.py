# producto/models.py

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagenes = models.ManyToManyField('Imagen', blank=True)
    contacto_de_referencia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='productos/')
    
    def __str__(self):
        return f"Imagen {self.id}"
