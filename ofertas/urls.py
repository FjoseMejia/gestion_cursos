from django.urls import path
from . import views

app_name = 'ofertas'
urlpatterns=[
    path("", views.index, name="index"),
    path("programas-sugeridos/", views.programas_sugeridos, name="programas-sugeridos"),
    path("duraciones-disponibles/", views.duraciones_disponibles, name="duraciones-disponibles"),
    path('fichas/', views.reporte_fichas_view, name='fichas'),
    path('solicitudes/', views.solicitudes_list_view, name='solicitudes_list'),
]