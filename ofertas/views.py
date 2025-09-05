from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from .models import ProgramaFormacion
from ofertas.forms import OfertaForm
from django.db.models import Count
from django.shortcuts import redirect
from openpyxl import Workbook
import io
from.models import  Oferta
from .models import Estado


# Create your views here.
@login_required
def index(request):
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

            oferta.estado = Estado.objects.get(id=1)
            oferta.save()
            messages.success(request, "¡Solicitud enviada correctamente!")
            return redirect('ofertas:index')
        else:
            messages.error(request, "Hubo un error al enviar la solicitud. Verifica los datos.")
            print(form.errors.as_json())
    else:
        form = OfertaForm()

    return render(
        request,
        'ofertas.html',
        {
            'grupo_nombre': grupo_nombre,
            'css_file': f'css/oferta_{grupo_nombre.lower()}.css',
            'js_file': f'js/oferta_{grupo_nombre.lower()}.js',
            'form': form,
            'duraciones': duraciones
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