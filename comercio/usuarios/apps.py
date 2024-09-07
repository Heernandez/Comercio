from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"
    name = 'usuarios'

    def ready(self):
        import usuarios.signals  # Importa las señales al iniciar la aplicación
