from django.contrib import admin
from .models import ProgramaEspecial, ModalidadPrograma, Oferta

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("id", "programa")


@admin.register(ProgramaEspecial)
class ProgramaEspecialAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")


@admin.register(ModalidadPrograma)
class ModalidadProgramaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")