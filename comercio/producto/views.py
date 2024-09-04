from django.http import HttpResponse,JsonResponse
from .models import Producto, Subproducto  # Cambié Variante por Subproducto
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from reserva.models import Reserva, ProductoReserva
import uuid  # Para generar un identificador único
from datetime import datetime


def generar_codigo_reserva():
    """Genera un código único para la reserva"""
    return f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

@csrf_exempt
def actualizar_stock(request):
    print("Actualizando stock")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        producto_id = data.get('productoId')
        cantidad_producto = data.get('cantidadProducto', 0)
        cantidades_subproductos = data.get('cantidadesSubproductos', {})

        try:
            # Obtener el usuario desde la solicitud o asignar uno por defecto
            usuario = request.user
            # Crear la reserva
            # Generar un código de reserva único
            codigo_reserva = generar_codigo_reserva()

            # Crear la reserva con el código generado
            reserva = Reserva.objects.create(
                codigo_reserva=codigo_reserva,
                usuario=usuario,
                cantidad_total=cantidad_producto,  # Actualizar más adelante
                valor_total=0.0  # Actualizar más adelante
            )

            valor_total = 0
            cantidad_total = 0

            producto = Producto.objects.get(id=producto_id)

            if cantidades_subproductos:
                # Actualizar el stock de los subproductos
                for subproducto_id, cantidad in cantidades_subproductos.items():
                    subproducto = Subproducto.objects.get(id=subproducto_id)
                    subproducto.stock_disponible -= cantidad
                    subproducto.save()

                    # Crear la instancia de ProductoReserva
                    ProductoReserva.objects.create(
                        reserva=reserva,
                        producto=subproducto.producto,
                        subproducto=subproducto,
                        cantidad=cantidad
                    )

                    # Acumular valor y cantidad total
                    valor_total += subproducto.precio * cantidad  # Asumiendo que el precio está en el modelo Producto
                    cantidad_total += cantidad

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

                # Crear la instancia de ProductoReserva
                ProductoReserva.objects.create(
                    reserva=reserva,
                    producto=producto,
                    cantidad=cantidad_producto
                )

                # Acumular valor y cantidad total
                valor_total += producto.precio_base * cantidad_producto
                cantidad_total += cantidad_producto

            # Actualizar cantidad_total y valor_total en la reserva
            reserva.cantidad_total = cantidad_total
            reserva.valor_total = valor_total
            reserva.save()

            return JsonResponse({'success': True, 'reserva_id': reserva.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def lista_productos(request):
    query = request.GET.get('search', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    return render(request, 'producto/producto.html', {'productos': productos})

@login_required
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


@login_required
def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'producto/producto.html', {'productos': productos})


@login_required
def producto_detalle(request, id):
    ambiente = settings.DEBUG
    producto = get_object_or_404(Producto, id=id)
    tiene_subproductos = producto.subproductos.exists()  
    if(producto.es_visible):
        return render(request, 'producto/detalle.html', {
            'producto': producto,
            'tiene_subproductos': tiene_subproductos,
            'ambiente': ambiente, 
        })
    else:
        return redirect(reverse('productos'))

def index(request):
    return HttpResponse("Página de inicio de la aplicación.")

def detalle(request):
    return HttpResponse("Página de detalle.")
