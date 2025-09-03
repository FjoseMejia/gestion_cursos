"""
URL configuration for inscripciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# inscripciones/urls.py
from django.contrib import admin
from django.urls import path

# Importa tus vistas para poder referenciarlas
from . import views 

urlpatterns = [
    # Todos los patrones de URL deben estar en una sola lista
    path('', views.inscripcion_formulario, name='index'),
    path('admin/', admin.site.urls),
    path('exportar-excel/', views.exportar_a_excel, name='exportar_excel'),
    path('exportar-personales/', views.exportar_datos_personales, name='exportar_personales'),

    # La URL para exportar el archivo de Excel
    #path('exportar-excel/', views.exportar_a_excel, name='exportar_excel'),
]