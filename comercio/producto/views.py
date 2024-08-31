# nombre_de_la_app/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse("Página de inicio de la aplicación.")

def detalle(request):
    return HttpResponse("Página de detalle.")
