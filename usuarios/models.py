
from django.contrib.auth.models import AbstractUser
from django.db import models

class TipoIdentificacion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Perfil(AbstractUser):
    # Campos adicionales obligatorios
    telefono = models.BigIntegerField(null=True, blank=True)
    tipo_identificacion = models.ForeignKey(
        TipoIdentificacion,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    numero_identificacion = models.CharField(max_length=50, null= True, blank= True)
    area = models.ForeignKey(
        Area, on_delete= models.PROTECT, null= True, blank= True
    )
    es_verificado = models.BooleanField(default= True)

    def __str__(self):
        return f"{self.username} - {self.email}"
