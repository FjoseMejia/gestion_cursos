from django.urls import path
from . import views
from .views import editar_estado_comentario

app_name= 'ofertas'
urlpatterns= [
    path("", views.index, name="index"),
<<<<<<< HEAD
    path("programas-sugeridos/", views.programas_sugeridos, name="programas-sugeridos"),
    path("duraciones-disponibles/", views.duraciones_disponibles, name="duraciones-disponibles"),
    path("solicitud/", views.solicitudes, name="solicitud"),
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path("reportes/export-excel/", views.exportar_a_excel, name='descargar'),
=======
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path('solicitud/', views.index, name='solicitud'),
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path('api/programas_sugeridos/', views.programas_sugeridos, name='programas_sugeridos'),
    path('cambiar-estado/<int:oferta_id>/<str:accion>/', views.cambiar_estado, name='cambiar_estado'),

>>>>>>> fran/ofertas
]

