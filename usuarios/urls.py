from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import Registro

app_name= "usuarios"
urlpatterns= [
    path("", views.login, name="login"),
    path("registro", Registro.as_view(), name="register"),
<<<<<<< HEAD
    path("recuperar_password/<str:email>", views.recovery_password, name="recovery_password"),
    path("instructores/", views.instructores, name="instructores"),
=======
    path("instructores/", views.list_user_by_area, name="instructores"),
>>>>>>> c124c7a (olvido contraseña con sus vistas)

]

