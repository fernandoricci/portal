from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Account, UserProfile

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una clave para su usuario'
    }))

    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Reingrese su clave'
    }))

    class Meta:
        model= Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    #Aplico estilos y ajusto atributos a los controles del formulario
    def __init__(self, *args, **kwargs):
        super(RegistroForm,self).__init__(*args, **kwargs)
        #Aplico placeholder individualmente a cada control
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese su nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese su apellido'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese su dirección de correo'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingrese su número de teléfono'

        #reccorro todos los controles para aplicar el estilo
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    #Limpio los datos ingrsados y manejo errores para mostrarlos en el template
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if password != confirmar_password:
            raise forms.ValidationError(
                "Las claves ingresadas no coinciden!"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields =('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ('Solo archivos de imagen')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'