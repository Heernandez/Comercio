# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nombre', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'nombre', 'apellido','email', 'is_staff')
    search_fields = ('username', 'nombre','apellido','email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
