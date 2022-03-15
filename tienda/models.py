from typing import Collection
from django.db import models
from django.forms import IntegerField
from coleccion.models import Coleccion

class Producto(models.Model):
    producto_nombre = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio = models.IntegerField()
    imagenes = models.ImageField(upload_to='photos/products')
    stock = IntegerField()
    is_available = models.BooleanField(default=True)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.producto_nombre
    