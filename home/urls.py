from django.urls import path
from . import views
from .views import home_funcionario

app_name= 'home'
urlpatterns= [
    path("", views.home, name="index"),
    path('funcionario/', home_funcionario, name='home_funcionario'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('reportes/', views.reportes, name='reportes'),    
]