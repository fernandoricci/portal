from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):

    icon_name = 'book'

    list_display = ('producto_nombre', 'precio', 'stock', 'coleccion', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('producto_nombre',)}

admin.site.register(Producto,ProductoAdmin)
