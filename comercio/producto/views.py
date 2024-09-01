from django.http import HttpResponse
from .models import Producto, Subproducto  # Cambié Variante por Subproducto
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        subproducto_id = request.POST.get('subproducto_id')  # Cambié variante_id por subproducto_id
        cantidad = int(request.POST.get('cantidad', 0))

        producto = get_object_or_404(Producto, id=producto_id)

        if subproducto_id:
            subproducto = get_object_or_404(Subproducto, id=subproducto_id)  # Cambié variante por subproducto
            if cantidad > subproducto.stock:
                return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)
            # Lógica para agregar el subproducto al carrito
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
    tiene_subproductos = producto.subproductos.exists()  # Cambié tiene_variantes por tiene_subproductos
    return render(request, 'producto/detalle.html', {
        'producto': producto,
        'tiene_subproductos': tiene_subproductos,  # Cambié tiene_variantes por tiene_subproductos
    })

def index(request):
    return HttpResponse("Página de inicio de la aplicación.")

def detalle(request):
    return HttpResponse("Página de detalle.")
