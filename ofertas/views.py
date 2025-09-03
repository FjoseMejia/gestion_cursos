from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import ProgramaFormacion
from ofertas.forms import OfertaForm

@login_required
def index(request):
    user= request.user
    grupo= user.groups.first()
    grupo_nombre= grupo.name if grupo else "Invitado"
    form= OfertaForm()
    duraciones = ProgramaFormacion.objects.values_list('duracion', flat=True).distinct().order_by('duracion')

    return render(
        request,
        'ofertas.html',
        {
            'css_file': f'css/oferta_{grupo_nombre.lower()}.css',
            'js_file':  f'js/oferta_{grupo_nombre.lower()}.js',
            'form': form,
            'duraciones': duraciones,
        }
    )

def programas_list(request):

    nombres = list(ProgramaFormacion.objects.values_list("nombre", flat=True))
    return JsonResponse({"nombres": nombres})

