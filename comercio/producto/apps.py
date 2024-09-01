from django.apps import AppConfig


class ProductoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "producto"
    
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        #ordering = ["-created"]
