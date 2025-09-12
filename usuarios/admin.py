
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import TipoIdentificacion, Area, Perfil


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Perfil)
class PerfilAdmin(UserAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email',
        'is_staff', 'is_active', 'es_verificado', 'get_grupos'
    )


    def get_grupos(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_grupos.short_description = "Grupos"



admin.site.unregister(Group)
admin.site.register(Group)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(TipoIdentificacion)
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
