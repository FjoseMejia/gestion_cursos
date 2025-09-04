from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse


role_home_map = {
    "SuperAdmin": "home/home_admin.html",
    "Funcionario": "home/home_funcionario.html",
    "Coordinador": "home/home_coordinador.html",
    "Instructor": "home/home_instructor.html",
    "Invitado": "home/home_invitado.html",
}
app_name= 'home'

@login_required
def home(request):
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else 'Invitado'

    if user.is_superuser:
        grupo_nombre = 'SuperAdmin'

    template = role_home_map.get(grupo_nombre, 'home/home_invitado.html')
    css_filename = f'css/home_{grupo_nombre.lower()}.css'

    return render(
        request,
        template,
        {
            'css_file': css_filename,
            'grupo_nombre': grupo_nombre,
        }
    )
