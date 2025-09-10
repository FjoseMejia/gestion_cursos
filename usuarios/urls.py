from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import Registro

app_name = "usuarios"

urlpatterns = [
    path("", views.login, name="login"),
    path("registro", Registro.as_view(), name="register"),
    path("instructores/", views.instructores, name="instructores"),
    path("instructores/nuevo/", views.crear_instructor, name="crear_instructor"),
    path("instructores/activar/<int:id>/", views.activar_instructor, name="activar_instructor"),
    
]

