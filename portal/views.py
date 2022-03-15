import imp
from django.shortcuts import render #importo renderizar y desplegar el codigo html producido por django

def home(request): 
    return render(request,'home.html') #devuelve el render del template home

