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
# Create your views here.
@login_required

def home(request):
    user = request.user
    grupo = user.groups.first()

    if grupo:
        grupo_nombre = grupo.name
    else:
        grupo_nombre = 'Sin grupo'


    if user.is_superuser:
        return render(
            request, 'home/home_admin.html',
            {
                'grupo_nombre': grupo_nombre,
                'css_file': 'css/home_admin.css'
            }
        )
    else:
        template = role_home_map.get(grupo_nombre)

    return render(
        request,
        template,
        {
            'css_file': f'css/home_{grupo_nombre.lower()}.css'
        }
    )

@login_required
def home_funcionario(request):
    from .models import Solicitud
    total = Solicitud.objects.count()
    aprobadas = Solicitud.objects.filter(estado="aprobada").count()
    pendientes = Solicitud.objects.filter(estado="pendiente").count()
    rechazadas = Solicitud.objects.filter(estado="rechazada").count()
    ultimas = Solicitud.objects.order_by('-fecha')[:5]
    return render(
        request,
        "home/home_funcionario.html",
        {
            "total": total,
            "aprobadas": aprobadas,
            "pendientes": pendientes,
            "rechazadas": rechazadas,
            "ultimas": ultimas,
            'css_file': 'css/home/funcionario.css'  # Si tienes un CSS específico, si no puedes quitar esta línea
        }
    )
@login_required
def solicitudes(request):
    return render(request, "home/solicitudes.html")

@login_required
def reportes(request):
    return render(request, "home/reportes.html")
