

from django.contrib import admin
from django.urls import path, include
from ofertas import views as ofertas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
<<<<<<< HEAD
=======
    path('', include('usuarios.urls_reset')),
>>>>>>> fran/ofertas
    path('usuarios/', include('usuarios.urls')),
    path('ofertas/', include('ofertas.urls')),
    path('inscripciones/', include('inscripciones.urls')),
]
