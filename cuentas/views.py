from base64 import urlsafe_b64encode
import email
from email import message
from email.message import EmailMessage
from multiprocessing import context
import profile
from django.forms import EmailInput
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistroForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

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

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            current_site = get_current_site(request)
            mail_subject = "Activa tu cuenta de la Libreria Virtual del INTA"
            body = render_to_string('cuentas/verificaciondecuenta.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            #messages.success(request, 'Se registro el usuario exitosamente')
            return redirect('/cuentas/login/?command=verification&email='+email)

    context = {
        'form': form
    }
    return render(request, 'cuentas/registro.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesión exitosamente')
            return redirect('perfil')
        else:
            messages.error(request, 'Las credenciales son incorrectas')
            return redirect('login')

    return render(request, 'cuentas/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Se ha cerrado la sesión")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta esta activa')
        return redirect('login')
    else:
        messages.error(request, 'La activación es inválidad')
        return redirect('registro')

@login_required(login_url='login')
def perfil(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context={
        'userprofile':userprofile,
    }

    return render(request, 'cuentas/perfil.html', context)


def olvidopassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
        
            current_site = get_current_site(request)
            mail_subject = "Recuperar contraseña - Libreria Virtual INTA"
            body = render_to_string('cuentas/resetear_clave_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request, 'Hemos enviado un correo electrónico a tu dirección de correo para que puedas reestablecer la contraseña')
            return redirect('login')

        else:
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect('olvidopassword')

    return render(request, 'cuentas/olvidopassword.html')


def resetearclave_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request, 'Por favor restablece tu contraseña')
        return redirect('resetearPassword')
    else:
        messages.error(request, 'El link ha expirado')
        return redirect('login')
    
def resetearPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Su clave se ha reestablecido con éxito')
            return redirect('login')
        else:
            messages.error(request, 'La contraseñas proporcionadas no concuerdan')
            return redirect('resetarPassword')
    else:
        return render(request, 'cuentas/resetearpassword.html')

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su información fue guardada con exito')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'cuentas/editarperfil.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact = request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'La contraseña se actualizo exitosamente')
                return redirect('change_password')
            else:
                messages.error(request, 'Por favor ingrese un password válido')
                return redirect('change_password')
        else:
            messages.error(request,'Las contraseñas no coinciden')
            return redirect('change_password')

    return render (request, 'cuentas/cambiarpassword.html')
