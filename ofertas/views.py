from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from .models import ProgramaFormacion,Estado,Oferta
from ofertas.forms import OfertaForm
from django.db.models import Count
from django.shortcuts import redirect
from .forms import InstructorArchivoForm, EstadoComentarioForm
from django.shortcuts import get_object_or_404
from .forms import SubirCedulaForm

@login_required
def subir_cedula_link(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)

    if request.method == 'POST':
        form = SubirCedulaForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo de cédulas subido correctamente.")
            return redirect('ofertas:index')  # Cambia esto según a dónde quieres redirigir
        else:
            messages.error(request, "Error al subir el archivo.")
    else:
        form = SubirCedulaForm(instance=oferta)

    return render(request, 'ofertas/subir_cedula_form.html', {'form': form, 'oferta': oferta})
def subir_cedula(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)

    # Validar que el usuario que sube el archivo sea el dueño
    if request.user != oferta.usuario:
        messages.error(request, "No tienes permiso para subir archivos a esta oferta.")
        return redirect('ofertas:solicitud')

    if request.method == 'POST':
        form = InstructorArchivoForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo de cédulas subido correctamente.")
            return redirect('ofertas:solicitud')
        else:
            messages.error(request, "Error al subir el archivo.")
    else:
        form = InstructorArchivoForm(instance=oferta)

    return render(request, 'ofertas/subir_cedula.html', {'form': form, 'oferta': oferta})
@login_required
def editar_estado_comentario(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else ""

    if grupo_nombre not in ["Funcionario", "Coordinador"]:
        messages.error(request, "No tienes permiso para modificar esta solicitud.")
        return redirect('ofertas:solicitudes')

    if request.method == 'POST':
        form = EstadoComentarioForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, "Estado y comentarios actualizados.")
            return redirect('ofertas:solicitudes')
        else:
            messages.error(request, "Error al actualizar la solicitud.")
    else:
        form = EstadoComentarioForm(instance=oferta)

    return render(request, 'ofertas/editar_estado_comentario.html', {'form': form, 'oferta': oferta})


# Create your views here.
@login_required
def cambiar_estado(request, oferta_id, accion):
    from .models import Oferta

    if request.method == "POST":
        try:
            oferta = Oferta.objects.get(id=oferta_id)
        except Oferta.DoesNotExist:
            messages.error(request, "La solicitud no existe.")
            return redirect('ofertas:index')

        comentario = request.POST.get("comentario", "")

        try:
            if accion == "aprobar":
                estado_nuevo = Estado.objects.get(nombre__iexact="Aprobado")
            elif accion == "rechazar":
                estado_nuevo = Estado.objects.get(nombre__iexact="Rechazado")
            elif accion == "devolver_instructor":
                estado_nuevo = Estado.objects.get(nombre__iexact="Devuelta al instructor")
            elif accion == "enviar_coordinador":
                estado_nuevo = Estado.objects.get(nombre__iexact="En revisión coordinador")
            elif accion == "devolver_funcionario":
                estado_nuevo = Estado.objects.get(nombre__iexact="Devuelta al funcionario")
            else:
                messages.error(request, "Acción no válida.")
                return redirect('ofertas:index')

            oferta.estado = estado_nuevo
            if comentario:
                # Solo guarda el comentario si se proporciona
                oferta.comentarios = comentario
            oferta.save()

            messages.success(request, f"Solicitud cambiada a '{estado_nuevo.nombre}'.")
        except Estado.DoesNotExist:
            messages.error(request, "Estado no encontrado.")
    return redirect('ofertas:index')  # Cambia a 'ofertas:index' si usas esa vista por defecto


def index(request):
    from .models import Oferta  # Asegúrate de importar Oferta aquí también

    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else "Invitado"
    duraciones = ProgramaFormacion.objects.values_list('duracion', flat=True).distinct().order_by('duracion')

    if request.method == "POST":
        form = OfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.usuario = user

            programa_id = request.POST.get('programa')
            if programa_id:
                try:
                    oferta.programa = ProgramaFormacion.objects.get(id=programa_id)
                except ProgramaFormacion.DoesNotExist:
                    messages.error(request, "El programa seleccionado no existe.")
                    return redirect('ofertas:index')

            try:
                oferta.estado = Estado.objects.get(id=1)  # Asegúrate de que exista el Estado con ID 1
            except Estado.DoesNotExist:
                messages.error(request, "Estado inicial no encontrado.")
                return redirect('ofertas:index')

            oferta.save()
            messages.success(request, "¡Solicitud enviada correctamente!")
            return redirect('ofertas:index')
        else:
            messages.error(request, "Hubo un error al enviar la solicitud. Verifica los datos.")
            print(form.errors.as_json())
    else:
        form = OfertaForm()

    # 🔍 MOSTRAR SOLICITUDES SEGÚN EL ROL
    if grupo_nombre == "Funcionario":
        solicitudes = Oferta.objects.all().order_by("creado_en")
    else:
        solicitudes = Oferta.objects.filter(usuario=user).order_by("creado_en")

    # ✅ SOLO UN RENDER
    return render(
        request,
        'ofertas.html',
        {
            'grupo_nombre': grupo_nombre,
            'css_file': f'css/oferta_{grupo_nombre.lower()}.css',
            'js_file': f'js/oferta_{grupo_nombre.lower()}.js',
            'form': form,
            'duraciones': duraciones,
            'solicitudes': solicitudes,
        }
    )


def programas_sugeridos(request):
    duracion = request.GET.get("duracion", "")

    programas = ProgramaFormacion.objects.all()

    if duracion:
        programas = programas.filter(duracion=duracion)

    data = [{"id": p.id, "nombre": p.nombre, "duracion": p.duracion} for p in programas]
    return JsonResponse(data, safe=False)

    
@login_required
def solicitudes(request):
    from .models import Oferta, Estado

    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else "Invitado"

    if grupo_nombre == "Instructor":
        # Instructor ve solo sus solicitudes
        solicitudes_list = Oferta.objects.filter(usuario=user).order_by('-creado_en')

    elif grupo_nombre == "Funcionario":
        try:
            estado_en_proceso = Estado.objects.get(nombre__iexact="En proceso")
        except Estado.DoesNotExist:
            messages.error(request, "El estado 'En proceso' no existe.")
            return redirect('ofertas:index')

        # Funcionario ve solicitudes "En proceso"
        solicitudes_list = Oferta.objects.filter(estado=estado_en_proceso).order_by('-creado_en')

    elif grupo_nombre == "Coordinador":
        try:
            estados_permitidos = Estado.objects.filter(
                nombre__in=["En proceso", "En revisión coordinador"]
            )
        except Estado.DoesNotExist:
            messages.error(request, "Algunos estados no existen.")
            return redirect('ofertas:index')

        solicitudes_list = Oferta.objects.filter(estado__in=estados_permitidos).order_by('-creado_en')

    else:
        solicitudes_list = Oferta.objects.filter(usuario=user).order_by('-creado_en')

    return render(
        request,
        "ofertas/solicitudes_usuario.html",
        {
            'solicitudes': solicitudes_list,
            'grupo_nombre': grupo_nombre,
            'css_file': 'css/solicitudes/funcionario.css' if grupo_nombre in ["Funcionario", "Coordinador"] else 'css/solicitudes/instructor.css',
        }
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

        for _ in range(int(cantidad)):
            ProgramaFormacion.objects.create(tipo_programa=tipo)
    return redirect('ofertas:reportes')
