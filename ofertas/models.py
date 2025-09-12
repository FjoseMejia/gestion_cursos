from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from smart_selects.db_fields import ChainedForeignKey


class NivelFormacion(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre

class RedConocimientos(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class LineaTecnologica(models.Model):
    nombre = models.CharField(max_length=255)

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

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre= models.CharField(max_length= 255)
    departamento= models.ForeignKey(Departamento, on_delete= models.PROTECT)

    def __str__(self):
        return self.nombre

class Corregimientos(models.Model):
    nombre= models.CharField(max_length=255)
    municipio= models.ForeignKey(Municipio, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Vereda(models.Model):
    nombre= models.CharField(max_length=255)
    corregimientos= models.ForeignKey(Corregimientos, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre


class Ambiente(models.Model):
    nombre= models.CharField(max_length=255)
    area_metros= models.IntegerField()

class Lugar(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)

    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",          # Campo en Lugar
        chained_model_field="departamento",    # Campo en Municipio
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
    )

    corregimientos = ChainedForeignKey(
        Corregimientos,
        chained_field="municipio",             # Campo en Lugar
        chained_model_field="municipio",       # Campo en Corregimientos
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
    )

    ambiente = models.CharField(max_length=255)

    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.direccion} ({self.municipio}, {self.departamento})"

#Se eliminó
class Jornada(models.Model):
    nombre = models.CharField(max_length=80)

class ModalidadPrograma(models.Model):
    nombre = models.CharField(max_length=28)

class Horario(models.Model):
    hora_inicio= models.TimeField()
    hora_fin= models.TimeField()

    def duracion(self):
        inicio= datetime.combine(datetime.today(), self.hora_inicio)
        fin= datetime.combine(datetime.today(), self.hora_fin)
        return fin - inicio

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"

class Dia(models.Model):
    nombre= models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class HorarioDia(models.Model):
    dia = models.ForeignKey(Dia, on_delete=models.PROTECT)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.dia.nombre}: {self.horario.hora_inicio}-{self.horario.hora_fin}"

class Estado(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class ProgramaEspecial(models.Model):
    nombre= models.CharField(max_length= 255)

    def __str__(self):
        return self.nombre

class EmpresaSolicitante(models.Model):
    nit= models.IntegerField()
    nombre= models.CharField(max_length= 255)
    subsector_economico= models.CharField(max_length= 255)

class Oferta(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    comentarios = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class ModalidadOferta(models.TextChoices):
        CAMPESENA = 'CAMPESENA', 'Campesena'
        REGULAR = 'REGULAR', 'Regular'

    modalidad_oferta = models.CharField(
        max_length=20,
        choices=ModalidadOferta.choices,
        default=ModalidadOferta.REGULAR
    )

    class TipoOferta(models.TextChoices):
        ABIERTA = 'ABIERTA', 'Abierta'
        CERRADA = 'CERRADA', 'Cerrada'

    tipo_oferta = models.CharField(
        max_length=10,
        choices=TipoOferta.choices,
        default=TipoOferta.ABIERTA
    )

    class EntornoGeografico(models.TextChoices):
        RURAL = 'RURAL', 'Rural'
        URBANO = 'URBANO', 'Urbano'

    entorno_geografico = models.CharField(
        max_length=10,
        choices=EntornoGeografico.choices,
        default=EntornoGeografico.URBANO
    )

    programa= models.ForeignKey("ProgramaFormacion", on_delete=models.PROTECT)
    modalidad_programa = models.ForeignKey("ModalidadPrograma", on_delete=models.PROTECT, blank=True, null=True)
    lugar = models.CharField(max_length=255, null=True, blank=True)  # <-- cambiado a texto
    horarios = models.ManyToManyField("Horario", related_name="ofertas", blank=True)
    estado = models.ForeignKey("Estado", on_delete=models.PROTECT)
    archivo= models.FileField(upload_to='cartas_solicitud/', default='', blank=True)
    cupo= models.IntegerField()
    empresa_solicitante = models.ForeignKey("EmpresaSolicitante", on_delete=models.PROTECT, null=True, blank=True)
    programa_especial = models.ForeignKey("ProgramaEspecial", on_delete=models.PROTECT, null=True, blank=True)
    ficha = models.CharField(max_length=255, null=True, blank=True)
    codigo_de_solicitud = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_terminacion = models.DateField(null=True, blank=True)
    fecha_de_inscripcion = models.DateField(null=True, blank=True)
    caracterizacion_generada= models.FileField(upload_to="ficha_caracterizacion/", blank=True, null=True)

    horario_dias = models.ManyToManyField(HorarioDia)

    def __str__(self):
        return f"Oferta {self.codigo_de_solicitud} - {self.tipo_oferta}"

    def calcular_fecha_terminacion(self):
        if not self.fecha_inicio or not self.programa or not self.horario_dias.exists():
            return None

        horas_semana = sum([
            hd.horario.duracion().total_seconds() / 3600
            for hd in self.horario_dias.all()
        ])

        if horas_semana <= 0:
            return None

        semanas = -(-self.programa.duracion // horas_semana)
        return self.fecha_inicio + timedelta(weeks=semanas)

    def save(self, *args, **kwargs):
        if self.fecha_inicio and self.programa and not self.pk:
            self.fecha_terminacion = None
        super().save(*args, **kwargs)


@receiver(m2m_changed, sender=Oferta.horario_dias.through)
def actualizar_fecha_terminacion(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        nueva_fecha = instance.calcular_fecha_terminacion()
        if nueva_fecha != instance.fecha_terminacion:
            instance.fecha_terminacion = nueva_fecha
            instance.save()