from django.db import models
from django.urls import reverse

class Coleccion(models.Model):
    coleccion_nombre = models.CharField(max_length=50, unique= True)
    descripcion = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    col_imagen = models.ImageField(upload_to = 'photos/colecciones', blank = True)

    class Meta:
        verbose_name = "coleccion"
        verbose_name_plural = "colecciones"

    def get_url(self):
        return reverse('productosporcoleccion',args=[self.slug])

    def __str__(self):
        return self.coleccion_nombre
    
