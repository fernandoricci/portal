from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name="tienda"),
    path('contacto/', views.contacto, name="contacto"),
    path('<slug:coleccion_slug>/', views.tienda, name='productosporcoleccion'),
    path('<slug:coleccion_slug>/<slug:producto_slug>/', views.producto_detalle, name='producto_detalle'),
]