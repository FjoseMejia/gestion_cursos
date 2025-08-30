from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def home(request):
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name

    role_home_map = {
        "SuperAdmin": "home/home_admin.html",
        "Funcionario": "home/home_funcionario.html",
        "Coordinador": "home/home_coordinador.html",
        "Instructor": "home/home_instructor.html",
        "Invitado": "home/home_invitado.html",
    }

    if user.is_superuser:
        return render(request, 'home/home_admin.html', {'grupo_nombre': grupo_nombre})
    else:
        template = role_home_map.get(grupo_nombre, "home/home_instructor.html")

    return render(request, template, {'grupo_nombre': grupo_nombre})

