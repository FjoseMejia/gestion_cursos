from django.contrib import admin
from .models import TipoIdentificacion, Area, Perfil

class AreaAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre')

class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display= ('id', 'nombre')

class PerfilAdmin(admin.ModelAdmin):
    exclude= ('date_joined', 'last_login')
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email',
        'is_staff', 'is_active', 'es_verificado', 'get_grupos'
    )

    def get_grupos(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_grupos.short_description = "Grupos"


# Register your models here.
admin.site.register(TipoIdentificacion, TipoIdentificacionAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Perfil, PerfilAdmin)
