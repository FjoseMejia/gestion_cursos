from django.urls import path
from . import views

app_name = 'ofertas'
urlpatterns = [
    path("", views.index, name="index"),
    path("programas-sugeridos/", views.programas_sugeridos, name="programas-sugeridos"),
    path("duraciones-disponibles/", views.duraciones_disponibles, name="duraciones-disponibles"),
    # path("solicitud/", views.solicitudes, name="solicitud"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),#cambio
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path("reportes/export-excel/", views.exportar_a_excel, name='descargar'),
]
