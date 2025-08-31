
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
    telefono = models.BigIntegerField(null=False, blank=False)
    tipo_identificacion = models.ForeignKey(
        TipoIdentificacion,
        on_delete=models.PROTECT,
        null=False,
        blank=False
    )
    numero_identificacion = models.CharField(max_length=50, null=False, blank=False)
    area = models.ForeignKey(
        Area, on_delete= models.PROTECT, null=False, blank=False
    )
    es_verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.email}"
