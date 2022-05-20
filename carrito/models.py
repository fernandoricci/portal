from django.db import models
from tienda.models import Producto

class Carrito(models.Model):
    carrito_id = models.CharField(max_length=250, blank=True)
    fecha_agregado = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carrito_id

class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    es_activo = models.BooleanField(default=True)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __unicode__(self):
        return self.producto
