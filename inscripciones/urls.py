
from django.contrib import admin
from django.urls import path

# Importa tus vistas para poder referenciarlas
from . import views 
app_name = 'inscripciones'

urlpatterns = [
    # Todos los patrones de URL deben estar en una sola lista
    path('', views.inscripcion_formulario, name='index'),
    path('exportar-excel/', views.exportar_a_excel, name='exportar_excel') ,
    path('exportar-personales/', views.exportar_datos_personales, name='exportar_personales'),
    path('detalle/<int:pk>/', views.detalle_inscripcion, name='detalle_inscripcion'),

    # La URL para exportar el archivo de Excel
    #path('exportar-excel/', views.exportar_a_excel, name='exportar_excel'),#
]