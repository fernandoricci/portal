from multiprocessing import context
from tkinter import E
from unicodedata import category
from urllib import request
from django.shortcuts import render, get_object_or_404
from .models import Producto
from coleccion.models import Coleccion

def tienda(request, coleccion_slug=None):
    colecciones = None
    productos = None

    if coleccion_slug != None:
        colecciones = get_object_or_404(Coleccion, slug=coleccion_slug)
        productos = Producto.objects.filter(coleccion=colecciones, is_available=True)
        productos_cuenta = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True)
        productos_cuenta = productos.count()

    context = {
        'productos': productos,
        'productos_cuenta': productos_cuenta,
    }


    return render(request, 'tienda/tienda.html', context)

def producto_detalle(request, coleccion_slug, producto_slug):
    try:
        #Valido que el producto exista
        producto_unico = Producto.objects.get(coleccion__slug = coleccion_slug, slug=producto_slug)
    except Exception as e:
        raise e

    #Si el producto_unico existe lo alamceno dentro de un diccionario "context"
    context = {
        'producto_unico': producto_unico,
    }
        
    return render(request, 'tienda/producto_detalle.html', context)

def contacto(request):
    return render(request, 'tienda/contacto.html')