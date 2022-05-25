from django.contrib import admin
from .models import Consulta
from .models import Respuesta

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 0


class ConsultaAdmin(admin.ModelAdmin):

    icon_name = 'contact_mail'    
    
    inlines = [RespuestaInline]

    list_display = [
            'estado_de_respuesta',
            'fecha',
            'nombre',
            'asunto',
            'mail',
            'telefono'
        ]

    list_filter = ['estado_respuesta', 'fecha']

admin.site.register(Consulta, ConsultaAdmin)