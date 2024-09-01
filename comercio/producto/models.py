# producto/models.py

from django.db import models

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='productos/')
    
    def __str__(self):
        return f"Imagen {self.id}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagenes = models.ManyToManyField(Imagen, blank=True, related_name='productos')
    contacto_de_referencia = models.CharField(max_length=100)
    stock_disponible = models.IntegerField(null=True, blank=True)  # Solo para productos sin variantes

    def __str__(self):
        return self.nombre

    def tiene_variantes(self):
        return self.variantes.exists()

    def stock_total(self):
        if self.tiene_variantes():
            return sum(variante.stock_disponible for variante in self.variantes.all())
        return self.stock_disponible

class Variante(models.Model):
    producto = models.ForeignKey(Producto, related_name='variantes', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Ejemplo: 'Fresa', 'Chocolate'
    stock_disponible = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Precio específico para esta variante (opcional)
    imagenes = models.ManyToManyField(Imagen, blank=True, related_name='variantes')

    def __str__(self):
        return f"{self.nombre} de {self.producto.nombre}"
