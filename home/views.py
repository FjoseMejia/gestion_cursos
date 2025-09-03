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

    grupo_nombre = grupo.name.capitalize() if grupo else 'Invitado'

    if user.is_superuser:
        return render(
            request,
            'home/home_admin.html',
            {
                'grupo_nombre': grupo_nombre,
                'css_file': 'css/home_admin.css'
            }
        )

    template = role_home_map.get(grupo_nombre, 'home/home_invitado.html')

    return render(
        request,
        template,
        {
            'css_file': f'css/home_{grupo_nombre.lower()}.css',
            'grupo_nombre': grupo_nombre,
        }
    )
