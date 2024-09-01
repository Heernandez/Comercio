# nombre_de_la_app/views.py

from django.http import HttpResponse
from .models import Producto,Variante
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse

def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        variante_id = request.POST.get('variante_id')
        cantidad = int(request.POST.get('cantidad', 0))

        producto = get_object_or_404(Producto, id=producto_id)

        if variante_id:
            variante = get_object_or_404(Variante, id=variante_id)
            if cantidad > variante.stock:
                return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)
            # Lógica para agregar la variante al carrito
        else:
            if cantidad > producto.stock:
                return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)
            # Lógica para agregar el producto al carrito

        return JsonResponse({'success': 'Producto agregado al carrito'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'producto/producto.html', {'productos': productos})

def producto_detalle(request, id):
    producto = get_object_or_404(Producto, id=id)
    a = list(producto.variantes.all())
    tiene_variantes = producto.variantes.exists()  # Verifica si existen variantes
    print(producto)
    return render(request, 'producto/detalle.html', {
        'producto': producto,
        'tiene_variantes': tiene_variantes,
    })

def index(request):
    return HttpResponse("Página de inicio de la aplicación.")

def detalle(request):
    return HttpResponse("Página de detalle.")
