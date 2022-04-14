from typing import Collection


from .models import Coleccion

def menu_links(request):
    links = Coleccion.objects.all()
    return dict(links=links)
    