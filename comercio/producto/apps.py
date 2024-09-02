from django.apps import AppConfig

class ProductoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "producto"
    verbose_name = "Producto"
    verbose_name_plural = "Productos"
