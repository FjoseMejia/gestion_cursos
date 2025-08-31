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

# Create your views here.
@login_required
def home(request):
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name



    if user.is_superuser:
        return render(request, 'home/home_admin.html', {'grupo_nombre': grupo_nombre})
    else:
        template = role_home_map.get(grupo_nombre)

    return render(request, template, {})