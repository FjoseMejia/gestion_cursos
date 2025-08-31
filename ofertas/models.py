from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class NivelFormacion(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class RedConocimientos(models.Model):
    nombre = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre


class LineaTecnologica(models.Model):
    nombre = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre

class ProgramaFormacion(models.Model):
    codigo= models.IntegerField()
    version= models.IntegerField()
    nombre= models.CharField(max_length=255)

    class TipoPrograma(models.TextChoices):
        COMPLEMENTARIA= 'COMPLEMENTARIA', 'Complementaria'
        TITULADA= 'TITULADA', 'Titulada'

    tipo_programa = models.CharField(
        max_length= 20,
        choices= TipoPrograma.choices,
        default= TipoPrograma.COMPLEMENTARIA
    )

    duracion= models.IntegerField()
    duracion_etapa_lectiva= models.IntegerField()
    duracion_etapa_productiva= models.IntegerField()
    estado= models.CharField(max_length=30)

    nivel_formacion = models.ForeignKey(
        NivelFormacion,
        on_delete=models.PROTECT,
        related_name='programas'
    )

    linea_tecnologica = models.ForeignKey(
        LineaTecnologica,
        on_delete=models.PROTECT,
        related_name='programas'
    )

    red_conocimiento = models.ForeignKey(
        RedConocimientos,
        on_delete=models.PROTECT,
        related_name='programas',
    )

    @property
    def duracion_total(self):
        return self.duracion_etapa_lectiva + self.duracion_etapa_productiva

    def __str__(self):
        return f"{self.nombre} ({self.tipo_programa})"


class Departamento(models.Model):
    nombre= models.CharField(max_length= 255)


class Municipio(models.Model):
    nombre= models.CharField(max_length= 255)
    departamento= models.ForeignKey(Departamento, on_delete= models.PROTECT)


class Corregimientos(models.Model):
    nombre= models.CharField(max_length=255)
    municipio= models.ForeignKey(Municipio, on_delete=models.PROTECT)

class Vereda(models.Model):
    nombre= models.CharField(max_length=255)
    corregimientos= models.ForeignKey(Corregimientos, on_delete=models.PROTECT)


class Ambiente(models.Model):
    nombre= models.CharField(max_length=255)
    area_metros= models.IntegerField()

class Lugar(models.Model):
    departamento= models.ForeignKey(Departamento, on_delete=models.PROTECT)
    municipio= models.ForeignKey(Municipio, on_delete=models.PROTECT)
    corregimientos= models.ForeignKey(Corregimientos, on_delete=models.PROTECT)
    direccion= models.CharField(max_length= 255)
    ambiente= models.ForeignKey(Ambiente, on_delete=models.PROTECT)


class Jornada(models.Model):
    nombre = models.CharField(max_length=80)


class Modalidad(models.Model):
    nombre = models.CharField(max_length=28)


class Horario(models.Model):
    jornada= models.ForeignKey(Jornada, on_delete=models.PROTECT)
    modalidad= models.ForeignKey(Modalidad, on_delete=models.PROTECT)
    hora_inicio= models.TimeField()
    hora_fin= models.TimeField()

    def duracion(self):
        inicio = datetime.combine(datetime.today(), self.hora_inicio)
        fin = datetime.combine(datetime.today(), self.hora_fin)
        return fin - inicio  # timedelta

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"

class Dia(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class HorarioDia(models.Model):
    dia = models.ForeignKey(Dia, on_delete=models.PROTECT)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.dia.nombre}: {self.horario.hora_inicio}-{self.horario.hora_fin}"

class Estado(models.Model):
    color= models.CharField(max_length= 15)
    nombre= models.CharField(max_length= 24)


class ProgramaEspecial(models.Model):
    nombre= models.CharField(max_length= 255)


class Oferta(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class ModalidadOferta(models.TextChoices):
        CAMPESENA = 'CAMPESENA', 'Campesena'
        REGULAR = 'REGULAR', 'Regular'

    modalidad_oferta = models.CharField(
        max_length=20,
        choices= ModalidadOferta.choices,
        default= ModalidadOferta.REGULAR
    )

    class TipoOferta(models.TextChoices):
        ABIERTA = 'ABIERTA', 'Abierta'
        CERRADA = 'CERRADA', 'Cerrada'

    tipo_oferta = models.CharField(
        max_length=10,
        choices=TipoOferta.choices,
        default= TipoOferta.ABIERTA
    )

    class EntornoGeografico(models.TextChoices):
        RURAL = 'RURAL', 'Rural'
        URBANO = 'URBANO', 'Urbano'

    entorno_geografico = models.CharField(
        max_length=10,
        choices=EntornoGeografico.choices,
        default= EntornoGeografico.URBANO
    )

    # Relaciones con otras tablas
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.PROTECT)
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT, null=True, blank=True)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    cupo = models.IntegerField()
    empresa_solicitante = models.CharField(max_length=255, null=True, blank=True)
    subsector = models.CharField(max_length=255, null=True, blank=True)
    programa_especial = models.ForeignKey(ProgramaEspecial, on_delete=models.PROTECT, null=True, blank=True)
    convenio = models.CharField(max_length=255, null=True, blank=True)
    ficha = models.CharField(max_length=255, null=True, blank=True)
    codigo_de_solicitud = models.CharField(max_length=100, null=True, blank=True)

    fecha_inicio = models.DateField()
    fecha_terminacion = models.DateField()
    fecha_de_inscripcion = models.DateField()

    def __str__(self):
        return f"Oferta {self.codigo_de_solicitud} - {self.tipo_oferta}"
