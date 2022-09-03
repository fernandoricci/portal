from ast import keyword
from multiprocessing import context
from unicodedata import category
from urllib import request
from django.shortcuts import render, get_object_or_404

from carrito.models import ItemCarrito
from carrito.views import _carrito_id
from .models import Producto
from coleccion.models import Coleccion
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

def tienda(request, coleccion_slug=None):
    colecciones = None
    productos = None
    productos_cantidad = 0

    if coleccion_slug != None:
        colecciones = get_object_or_404(Coleccion, slug=coleccion_slug)
        productos = Producto.objects.filter(coleccion=colecciones, is_available=True).order_by('id')
        paginador = Paginator(productos, 3)
        pagina = request.GET.get('page')
        productos_paginados = paginador.get_page(pagina)
        productos_cantidad = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True).order_by('id')
        paginador = Paginator(productos, 6)
        pagina = request.GET.get('page')
        productos_paginados = paginador.get_page(pagina)
        productos_cuenta = productos.count()

    context = {
        'productos': productos_paginados,
        'productos_cantidad': productos_cantidad,
    }


    return render(request, 'tienda/tienda.html', context)

def producto_detalle(request, coleccion_slug, producto_slug):
    try:
        #Valido que el producto exista
        producto_unico = Producto.objects.get(coleccion__slug = coleccion_slug, slug=producto_slug)
        en_carrito = ItemCarrito.objects.filter(carrito__carrito_id=_carrito_id(request), producto=producto_unico).exists()
    except Exception as e:
        raise e

    #Si el producto_unico existe lo alamceno dentro de un diccionario "context"
    context = {
        'producto_unico': producto_unico,
        'en_carrito': en_carrito,
    }
        
    return render(request, 'tienda/producto_detalle.html', context)

def busqueda(request):
    productos = None
    productos_cantidad = 0
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            productos = Producto.objects.order_by('-created_date').filter(Q(descripcion__icontains=keyword)|Q(producto_nombre__icontains=keyword))
            productos_cantidad = productos.count()
    context={
        'productos': productos,
        'productos_cantidad': productos_cantidad,
    }

    return render (request, 'tienda/tienda.html', context)


def contacto(request):
    return render(request, 'tienda/contacto.html')