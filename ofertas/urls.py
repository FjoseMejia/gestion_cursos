from django.urls import path
from . import views
from .views import subir_cedula, editar_estado_comentario, subir_cedula_link

app_name = 'ofertas'
urlpatterns = [
    path("", views.index, name="index"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path('solicitud/', views.index, name='solicitud'),  # 👈 esto resuelve el problema sin afectar nada
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path('api/programas_sugeridos/', views.programas_sugeridos, name='programas_sugeridos'),
    path('cambiar-estado/<int:oferta_id>/<str:accion>/', views.cambiar_estado, name='cambiar_estado'),
    path('oferta/<int:oferta_id>/subir_cedula/', subir_cedula, name='subir_cedula'),
    path('oferta/<int:oferta_id>/subir_cedula/', subir_cedula_link, name='subir_cedula'),
    path('oferta/<int:oferta_id>/editar_estado/', editar_estado_comentario, name='editar_estado_comentario'),
]

