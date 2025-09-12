from django.contrib import admin
from .models import (
    ProgramaEspecial,
    ModalidadPrograma,
    Oferta,
    Dia,
    Departamento,
    Municipio,
    Corregimientos,
    Vereda
)


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("id", "programa")


@admin.register(ProgramaEspecial)
class ProgramaEspecialAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")


@admin.register(ModalidadPrograma)
class ModalidadProgramaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")

@admin.register(Dia)
class DiaAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre')

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre', 'departamento')

@admin.register(Corregimientos)
class CorregimientosAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre', 'municipio')

@admin.register(Vereda)
class VeredaAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre', 'corregimientos')
