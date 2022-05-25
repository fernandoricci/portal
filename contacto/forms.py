from dataclasses import field
import imp
from django import forms
from django.forms import ModelForm
from contacto.models import Consulta
from captcha.fields import CaptchaField

class ConsultaForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Consulta
        fields = [
            'nombre',
            'asunto',
            'mail',
            'telefono',
            'mensaje'
        ]
    
    #Aplico estilos y ajusto atributos a los controles del formulario
    def __init__(self, *args, **kwargs):
        super(ConsultaForm,self).__init__(*args, **kwargs)
        #Aplico placeholder individualmente a cada control
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese su nombre'
        self.fields['asunto'].widget.attrs['placeholder'] = 'Asunto'
        self.fields['mail'].widget.attrs['placeholder'] = 'Ingrese su dirección de correo'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese su número de teléfono'
        self.fields['mensaje'].widget.attrs['placeholder'] = 'Por favor deje su mensaje aquí'
        self.fields['captcha'].widget.attrs['placeholder'] = 'Complete el codigo que ve en la imagen'

