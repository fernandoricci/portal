from datetime import datetime
from django.db import models
from django.utils.html import format_html

class Consulta(models.Model): 

    constestada = 'Contestada'
    noconstestada = 'Sin contestar'
    enproceso = 'En proceso'

    estados = (
        (constestada, 'Contestada'),
        (noconstestada, 'Sin contestar'),
        (enproceso, 'En proceso'),
    )

    nombre = models.CharField(max_length=50, blank=False)
    asunto = models.CharField(max_length=50, blank=False)
    mail = models.EmailField(max_length=100)
    estado_respuesta = models.CharField(max_length=15, blank=True, null=True, choices=estados, default=noconstestada)
    telefono = models.CharField(max_length=50, blank=True,null=True)
    fecha = models.DateField(default=datetime.now, blank=True, editable=True)
    mensaje = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.nombre

    def estado_de_respuesta(self, ):
        if self.estado_respuesta == 'Contestada':
            return format_html('<span style="background-color:#369363; color:#fff; padding:5px;">{}</span>', self.estado_respuesta)

        elif self.estado_respuesta == 'Sin contestar':
            return format_html('<span style="background-color:#C6023F; color:#fff; padding:5px;">{}</span>', self.estado_respuesta)

        elif self.estado_respuesta == 'En proceso':
            return format_html('<span style="background-color:#61A1DE; color:#000; padding:5px;">{}</span>', self.estado_respuesta)

class Respuesta(models.Model):

    consulta = models.ForeignKey(Consulta(), blank=True, editable=True, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=False, null=False)
    fecha = models.DateField(default=datetime.now, blank=True, editable=True)
    
    def create_mensaje(self,):
        estado_consulta = Consulta.objects.get(id=self.consulta.id)
        estado_consulta.estado_respuesta = 'Contestada'
        estado_consulta.save()
        #LOGICA DE ENVIO DE MAIL DE LA RESPUESTA

    def save(self, *args, **kwargs):
        self.create_mensaje()
        force_update = False
        if self.id:
            force_update = True
        super(Respuesta, self).save(force_update=force_update)
