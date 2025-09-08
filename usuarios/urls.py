from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import Registro

app_name= "usuarios"
urlpatterns= [
    path("", views.login, name="login"),
    path("registro", Registro.as_view(), name="register"),
    path("instructores/", views.instructores, name="instructores"),
]

