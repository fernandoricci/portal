from django.shortcuts import redirect, render
from .forms import RegistroForm
from .models import Account
from django.contrib import messages

def registro(request):
    form = RegistroForm()

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            
            #compongo el username separando la primera parte de su direccion de mail
            username = email.split('@')[0]

            user= Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Se registro el usuario exitosamente')
            return redirect('registro')

    context = {
        'form': form
    }
    return render(request, 'cuentas/registro.html', context)

def login(request):
    return render(request, 'cuentas/login.html')

def logout(request):
    return
