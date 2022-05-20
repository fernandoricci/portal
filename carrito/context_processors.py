from .models import Carrito, ItemCarrito
from .views import _carrito_id

def counter(request):
    carrito_cuenta=0

    try:
        carrito = Carrito.objects.filter(carrito_id=_carrito_id(request))
        itemscarrito = ItemCarrito.objects.all().filter(carrito=carrito[:1])
        for itemcarrito in itemscarrito:
            carrito_cuenta += itemcarrito.cantidad
    except Carrito.DoesNotExist:
        carrito_cuenta=0
    return dict(carrito_cuenta=carrito_cuenta)