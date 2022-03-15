from django.contrib import admin
from .models import Coleccion

class ColeccionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('coleccion_nombre',)}
    list_display = ('coleccion_nombre', 'slug')


admin.site.register(Coleccion, ColeccionAdmin)
