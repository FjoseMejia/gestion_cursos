# inscripciones/models.py
from django.db import models

class Inscripcion(models.Model):
    TIPO_IDENTIFICACION_CHOICES = [
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de Ciudadanía'),
    ]
    
    tipo_identificacion = models.CharField(
        max_length=2,
        choices=TIPO_IDENTIFICACION_CHOICES,
        default='CC',
        verbose_name='Tipo de Identificación'
    )
    numero_identificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Identificación'
    )
    tipo_poblacion_aspirante = models.CharField(
        max_length=100,
        verbose_name='Tipo Población Aspirante'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.numero_identificacion} ({self.tipo_poblacion_aspirante})'