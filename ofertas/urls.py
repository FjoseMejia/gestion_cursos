from django.urls import path
from . import views

app_name = 'ofertas'
urlpatterns = [
    path("", views.index, name="index"),
    path("solicitud/", views.solicitudes, name="solicitud"),
    path("reportes/", views.reportes, name='reportes'),
    path("reportes/crear/", views.crear_reporte, name='crear_reporte'),
    path("reportes/export-excel/", views.exportar_a_excel, name='descargar'),
    path('/api/programas_sugeridos/', views.programas_sugeridos, name='programas_sugeridos'),
]
