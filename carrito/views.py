import re
from django.shortcuts import get_object_or_404, redirect, render
from carrito.models import Carrito, ItemCarrito
from tienda.models import Producto
from django.core.exceptions import ObjectDoesNotExist

def _carrito_id(request):
    carrito = request.session.session_key
    if not carrito:
        carrito= request.session.create()
    return carrito

def agregar_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
    except Carrito.DoesNotExist:
        carrito = Carrito.objects.create(
            carrito_id = _carrito_id(request)
        )
    carrito.save()

    try:
        itemcarrito = ItemCarrito.objects.get(producto=producto, carrito=carrito)
        itemcarrito.cantidad += 1
        itemcarrito.save()
    except ItemCarrito.DoesNotExist:
        itemcarrito = ItemCarrito.objects.create(
            producto = producto,
            cantidad = 1,
            carrito = carrito,
        )
        itemcarrito.save()
    return redirect('carrito')

#Función para disminuir la cantidad de un item hasta eliminarlo del carrito
def quitar_carrito(request, producto_id):
    carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
    producto = get_object_or_404(Producto, id=producto_id)
    itemcarrito= ItemCarrito.objects.get(producto=producto, carrito=carrito)

    if itemcarrito.cantidad > 1:
        itemcarrito.cantidad -=1
        itemcarrito.save()
    else:
        itemcarrito.delete()

    return redirect('carrito')

#Función para eliminar un item del carrito independientemente de la cantidad que tenga 
def quitar_item(request, producto_id):
    carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
    producto = get_object_or_404(Producto, id=producto_id)
    itemcarrito= ItemCarrito.objects.get(producto=producto, carrito=carrito)

    itemcarrito.delete()
    return redirect('carrito')

def carrito(request, total=0, cantidad=0, itemscarrito=None):
    iva=0
    preciofinal=0
    try:
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
        itemscarrito = ItemCarrito.objects.filter(carrito=carrito, es_activo=True)
        for itemcarrito in itemscarrito:
            total += (itemcarrito.producto.precio * itemcarrito.cantidad)
            cantidad += itemcarrito.cantidad
        iva = (21*total)/100
        preciofinal = total+iva

    except ObjectDoesNotExist:
        pass #solo ingoro la excepción

    context = {
        'total' : total,
        'cantidad' : cantidad,
        'itemscarrito': itemscarrito,
        'iva': iva,
        'preciofinal': preciofinal,
    }

    return render(request, 'tienda/carrito.html', context)
