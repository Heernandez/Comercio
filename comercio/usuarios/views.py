# usuarios/views.py

from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.conf import settings
import json

def register(request):
    if request.method == 'POST':
        # Maneja la solicitud POST y los datos JSON
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("lucho:\n",data)
            form = CustomUserCreationForm(data)
            if form.is_valid():
                user = form.save()
                #login(request, user)  # Inicia sesión automáticamente al registrar
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)}, status=500)
    else:
        # Maneja la solicitud GET
        form = CustomUserCreationForm()
    ambiente = settings.DEBUG
    return render(request, 'usuarios/register.html', {'form': form, 'ambiente': ambiente})


