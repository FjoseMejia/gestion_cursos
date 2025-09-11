from django.urls import path
from . import views
from .views import editar_estado_comentario

app_name= 'ofertas'
urlpatterns= [
    path("", views.index, name="index"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path('solicitud/', views.index, name='solicitud'),
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/exportar/", views.exportar_a_excel, name="exportar_a_excel"),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path('api/programas_sugeridos/', views.programas_sugeridos, name='programas_sugeridos'),
    path('cambiar-estado/<int:oferta_id>/<str:accion>/', views.cambiar_estado, name='cambiar_estado'),

]

