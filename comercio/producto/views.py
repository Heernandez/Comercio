from django.http import HttpResponse,JsonResponse
from .models import Producto, Subproducto  # Cambié Variante por Subproducto
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def actualizar_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        producto_id = data.get('productoId')
        cantidad_producto = data.get('cantidadProducto', 0)
        cantidades_subproductos = data.get('cantidadesSubproductos', {})

        try:
            if cantidades_subproductos:
                # Actualizar el stock de los subproductos
                for subproducto_id, cantidad in cantidades_subproductos.items():
                    subproducto = Subproducto.objects.get(id=subproducto_id)
                    subproducto.stock_disponible -= cantidad
                    subproducto.save()

                # Calcular el stock total de todos los subproductos y actualizar el producto
                producto = Producto.objects.get(id=producto_id)
                subproductos = Subproducto.objects.filter(producto=producto)
                total_stock_subproductos = sum([sub.stock_disponible for sub in subproductos])
                producto.stock_disponible = total_stock_subproductos
                producto.save()
            else:
                # Si no hay subproductos, actualizar el stock del producto principal
                producto = Producto.objects.get(id=producto_id)
                producto.stock_disponible -= cantidad_producto
                producto.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def lista_productos(request):
    query = request.GET.get('search', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    return render(request, 'producto/producto.html', {'productos': productos})

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
