# signals.py
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def add_to_user_group(sender, instance, created, **kwargs):
    if created:
        # Asignar el usuario al grupo PerfilDeUsuario
        group = Group.objects.get(name='comun')
        instance.groups.add(group)
