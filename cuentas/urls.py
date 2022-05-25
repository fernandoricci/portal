from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('', views.perfil, name='perfil'),
    path('olvidopassword/', views.olvidopassword, name='olvidopassword'),
    path('resetearpassword/', views.resetearPassword, name='resetearPassword'),
    path('resetearpasswordvalidate/<uidb64>/<token>/', views.resetearclave_validate, name='resetearclave_validate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
