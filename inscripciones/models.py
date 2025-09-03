# inscripciones/models.py
from django.db import models

class Inscripcion(models.Model):

    nombre = models.CharField(max_length=100, default='Sin nombre')
    apellido = models.CharField(max_length=100, default='Sin apellido')
    celular = models.CharField(max_length=15, default='0000000000')


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
    TIPO_POBLACION_ASPIRANTE_CHOICES = [
        ('Ninguna', 'Ninguna'),
        ('Víctima del conflicto', 'Víctima del conflicto'),
        ('Madre cabeza de familia', 'Madre cabeza de familia'),
        ('Afrocolombiano', 'Afrocolombiano'),
        ('Indígena', 'Indígena'),
        ('Discapacitado', 'Discapacitado'),
        ('Desplazado por la violencia', 'Desplazado por la violencia'),
    ]
    tipo_poblacion_aspirante = models.CharField(
        max_length=100,
        choices=TIPO_POBLACION_ASPIRANTE_CHOICES,
        default='Ninguna',
        verbose_name='Tipo Población Aspirante'
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.numero_identificacion} ({self.tipo_poblacion_aspirante})'