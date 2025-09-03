from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import ProgramaFormacion
from ofertas.forms import OfertaForm
from django.db.models import Count
from django.shortcuts import redirect


# Create your views here.
@login_required
def index(request):
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else "Invitado"
    form = OfertaForm()

    return render(
        request,
        'ofertas.html',
        {
            'grupo_nombre': grupo_nombre,
            'css_file': f'css/oferta_{grupo_nombre.lower()}.css',
            'js_file': f'js/oferta_{grupo_nombre.lower()}.js',
            'form': form
        }
    )

def duraciones_disponibles(request):
    duraciones = ProgramaFormacion.objects.values_list('duracion', flat=True).distinct().order_by('duracion')
    return JsonResponse(list(duraciones), safe=False)

def programas_sugeridos(request):
    duracion = request.GET.get("duracion", "")

    programas = ProgramaFormacion.objects.all()

    if duracion:
        programas = programas.filter(duracion=duracion)

    data = [{"id": p.id, "nombre": p.nombre, "duracion": p.duracion} for p in programas]
    return JsonResponse(data, safe=False)

@login_required
def solicitudes(request):
    # from .models import Solicitud
    # total = Solicitud.objects.count()
    # aprobadas = Solicitud.objects.filter(estado="aprobada").count()
    # pendientes = Solicitud.objects.filter(estado="pendiente").count()
    # rechazadas = Solicitud.objects.filter(estado="rechazada").count()
    # ultimas = Solicitud.objects.order_by('-fecha')[:5]
    return render(
        request,
        "solicitud.html",
        # {
        #     "total": total,
        #     "aprobadas": aprobadas,
        #     "pendientes": pendientes,
        #     "rechazadas": rechazadas,
        #     "ultimas": ultimas,
        #     'css_file': 'css/solicitudes/funcionario.css'  # Si tienes un CSS específico, si no puedes quitar esta línea
        # }
    )


@login_required
def reportes(request):
    # Contar fichas por tipo (campesena, regular, etc.)
    fichas_por_tipo = ProgramaFormacion.objects.values('tipo_programa').annotate(total=Count('id'))

    # Si quieres además totales separados
    campesena = ProgramaFormacion.objects.filter(tipo_programa="campesena").count()
    regular = ProgramaFormacion.objects.filter(tipo_programa="regular").count()
    total = ProgramaFormacion.objects.count()


    return render(request, 'reportes.html', { 'css_file': 'css/reportes.css',
        'fichas_por_tipo': fichas_por_tipo,
        'campesena': campesena,
        'regular': regular,
        'total': total,
    })

@login_required
def crear_reporte(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo_programa")
        cantidad = request.POST.get("cantidad")
        # Guardar el reporte en la tabla ProgramaFormacion
        for _ in range(int(cantidad)):
            ProgramaFormacion.objects.create(tipo_programa=tipo)
    return redirect('ofertas:reportes')
