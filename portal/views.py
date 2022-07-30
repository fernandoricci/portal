from django.shortcuts import render #importo renderizar y desplegar el codigo html producido por django
from tienda.models import Producto

def home(request):
    productos = Producto.objects.all().filter(is_available=True)
    
    context = {
        'productos': productos,
    }

    return render(request,'home.html', context) #devuelve el render del template home

