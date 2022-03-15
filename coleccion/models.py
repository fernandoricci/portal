from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models

class Coleccion(models.Model):
    coleccion_nombre = models.CharField(max_length=50, unique= True)
    descripcion = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    col_imagen = models.ImageField(upload_to = 'photos/colecciones', blank = True)

    class Meta:
        verbose_name = "coleccion"
        verbose_name_plural = "colecciones"

    def __str__(self):
        return self.coleccion_nombre
    
