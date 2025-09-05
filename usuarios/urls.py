from django.urls import path
from . import views
from .views import Registro

app_name = "usuarios"

urlpatterns = [
    path("", views.login, name="login"),
    path("registro", Registro.as_view(), name="register"),
    path("recuperar_password/<str:email>", views.recovery_password, name="recovery_password"),
    path("instructores/", views.instructores, name="instructores"),

    # 🔹 Nueva ruta para crear instructor
    path("instructores/nuevo/", views.crear_instructor, name="crear_instructor"),
]
