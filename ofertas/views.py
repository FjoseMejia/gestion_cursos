from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from .utils import generar_ficha
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Oferta, ProgramaFormacion, Estado, Horario, HorarioDia
from .forms import OfertaForm, LugarForm

def index(request):
    user = request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else "Invitado"
    duraciones = ProgramaFormacion.objects.values_list(
        'duracion', flat=True
    ).distinct().order_by('duracion')

    if request.method == "POST":
        form = OfertaForm(request.POST, request.FILES)
        lugar_form = LugarForm(request.POST)

        if form.is_valid() and lugar_form.is_valid():
            oferta = form.save(commit=False)
            oferta.usuario = user

            # programa
            programa_id = request.POST.get('programa')
            if programa_id:
                try:
                    oferta.programa = ProgramaFormacion.objects.get(id=programa_id)
                except ProgramaFormacion.DoesNotExist:
                    messages.error(request, "El programa seleccionado no existe.")
                    return redirect('ofertas:index')

            # estado inicial
            try:
                oferta.estado = Estado.objects.get(id=1)
            except Estado.DoesNotExist:
                messages.error(request, "Estado inicial no encontrado.")
                return redirect('ofertas:index')

            oferta.save()

            hora_inicio = form.cleaned_data.get('hora_inicio')
            hora_fin = form.cleaned_data.get('hora_fin')
            dias = form.cleaned_data.get('dias')

            if hora_inicio and hora_fin and dias:
                horario = Horario.objects.create(
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                for dia in dias:
                    hd = HorarioDia.objects.create(dia=dia, horario=horario)
                    oferta.horario_dias.add(hd)

            # generar documento
            ruta = generar_ficha(oferta)
            oferta.archivo = ruta
            oferta.save()

            messages.success(request, "Solicitud creada y documento generado.")
            return redirect('ofertas:index')
        else:
            messages.error(request, "Hubo un error al enviar la solicitud. Verifica los datos.")
            print(form.errors.as_json())
    else:
        form = OfertaForm()
        lugar_form = LugarForm()

    # solicitudes según rol
    if grupo_nombre == "Funcionario":
        solicitudes = Oferta.objects.all().order_by("creado_en")
    else:
        solicitudes = Oferta.objects.filter(usuario=user).order_by("creado_en")


    return render(
        request,
        'oferta.html',
        {
            'grupo_nombre': grupo_nombre,

            'css_file': 'css/oferta.css',
            'js_file': 'js/oferta.js',
            'form': form,
            'lugar_form': lugar_form,
            'duraciones': duraciones,
            'solicitudes': solicitudes,
        }
    )

def duraciones_disponibles(request):
    duraciones = ProgramaFormacion.objects.values_list('duracion', flat=True).distinct().order_by('duracion')
    return JsonResponse(list(duraciones), safe=False)

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

    fichas_por_tipo = ProgramaFormacion.objects.values('tipo_programa').annotate(total=Count('id'))

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
    
def exportar_a_excel(request):
    datos = (
        Oferta.objects
        .select_related("empresa_solicitante", "estado", "usuario", "programa")
        .filter(programa__nombre__in=["CAMPESENA", "REGULAR"])
        .values(
            'codigo_de_solicitud',
            'modalidad_oferta',
            'tipo_oferta',
            'entorno_geografico',
            'cupo',
            'ficha',
            'fecha_inicio',
            'fecha_terminacion',
            'fecha_de_inscripcion',
            'empresa_solicitante__nombre',
            'estado__nombre',
            'usuario__first_name',
            'usuario__last_name',
            'programa__nombre',
        )
        .order_by('id')
    )

    output = io.BytesIO()
    workbook = Workbook()
    sheet = workbook.active

    # Encabezados
    sheet['A1'] = 'Código solicitud'
    sheet['B1'] = 'Modalidad'
    sheet['C1'] = 'Tipo'
    sheet['D1'] = 'Entorno'
    sheet['E1'] = 'Cupo'
    sheet['F1'] = 'Ficha'
    sheet['G1'] = 'Fecha inicio'
    sheet['H1'] = 'Fecha terminación'
    sheet['I1'] = 'Fecha inscripción'
    sheet['J1'] = 'Empresa'
    sheet['K1'] = 'Estado'
    sheet['L1'] = 'Usuario Nombre'
    sheet['M1'] = 'Usuario Apellido'
    sheet['N1'] = 'Tipo Programa'

    # Llenar los datos en cada fila
    row_num = 2
    for values in datos:
        sheet[f'A{row_num}'] = values['codigo_de_solicitud']
        sheet[f'B{row_num}'] = values['modalidad_oferta']
        sheet[f'C{row_num}'] = values['tipo_oferta']
        sheet[f'D{row_num}'] = values['entorno_geografico']
        sheet[f'E{row_num}'] = values['cupo']
        sheet[f'F{row_num}'] = values['ficha']
        sheet[f'G{row_num}'] = values['fecha_inicio']
        sheet[f'H{row_num}'] = values['fecha_terminacion']
        sheet[f'I{row_num}'] = values['fecha_de_inscripcion']
        sheet[f'J{row_num}'] = values['empresa_solicitante__nombre']
        sheet[f'K{row_num}'] = values['estado__nombre']
        sheet[f'L{row_num}'] = values['usuario__first_name']
        sheet[f'M{row_num}'] = values['usuario__last_name']
        sheet[f'N{row_num}'] = values['programa__nombre']
        row_num += 3

    #  Resumen al final
    campesena = Oferta.objects.filter(programa__nombre="CAMPESENA").count()
    regular = Oferta.objects.filter(programa__nombre="REGULAR").count()
    total = Oferta.objects.count()

    sheet[f'A{row_num+1}'] = "Totales"
    sheet[f'A{row_num+2}'] = "Campesena"
    sheet[f'B{row_num+2}'] = campesena
    sheet[f'A{row_num+3}'] = "Regular"
    sheet[f'B{row_num+3}'] = regular
    sheet[f'A{row_num+4}'] = "Total"
    sheet[f'B{row_num+4}'] = total

    # Guardar y enviar
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="inscripciones.xlsx"'

    return response

    """Genera y descarga un archivo de Excel con los datos de todas las inscripciones."""
    datos =Oferta.objects.select_related(oferta__nombre="CAMPESENA").values('modalidad_oferta', 'tipo_oferta', 'entorno_geografico', 'cupo', 'subsector', 'convenio', 'ficha', 'codigo_de_solicitud', 'fecha_icinio', 'fecha_terminacion', 'fecha_inscripcion', ).order_by('id')

    output = io.BytesIO()
    workbook = Workbook()
    sheet = workbook.active

    # Define los encabezados de las columnas
    sheet['A1'] = 'id'
    sheet['B1'] = 'nombre'
    # sheet['C1'] = 'instructor'
    # sheet['D1'] = 'modalidad '
    # sheet['E1'] = 'Código de la Ficha'
    # sheet['F1'] = 'fehca de inicio'
    # sheet['G1'] = 'fecha de fin'
 

    # Ancho de las columnas para que se vean bien
    sheet.column_dimensions['A'].width = 25
    sheet.column_dimensions['B'].width = 25
    # sheet.column_dimensions['C'].width = 25
    # sheet.column_dimensions['D'].width = 20
    # sheet.column_dimensions['E'].width = 30
    # sheet.column_dimensions['F'].width = 20
    # sheet.column_dimensions['G'].width = 20

    # Llena los datos en las filas correspondientes
    row_num = 2
    for values in datos:
        sheet[f'A{row_num}'] = values.id
        sheet[f'B{row_num}'] = values.nombre
        # sheet[f'E{row_num}'] = ModalidadOferta.tipo_poblacion_aspirante
        row_num += 1

    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="inscripciones.xlsx"'

    return response

def solicitudes (request):
    return render(
            request,
            'solicitudes/solicitudes.html',
            {
                
                'css_file': 'solicitudes/css/solicitudes.css',
                'js_file': 'solicitudes/js/solicitudes.js',
            }
    )

