# inscripciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import InscripcionForm
from .models import Inscripcion
from openpyxl import Workbook
import io
from .models import Inscripcion  # <-- Asegúrate de que este modelo exista

def inscripcion_formulario(request):
    LIMITE_CUPOS = 25
    total_inscritos = Inscripcion.objects.count()

    if request.method == 'POST':
        if total_inscritos >= LIMITE_CUPOS:
            # Si ya no hay cupos, no se guarda y se muestra mensaje
            form = InscripcionForm()
        else:
            form = InscripcionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('inscripciones')  # Redirige para evitar reenvío
    else:
        form = InscripcionForm()

    # Mensaje de cupos
    if total_inscritos >= LIMITE_CUPOS:
        mensaje_cupos = "❌ No existen cupos disponibles para este curso. El límite de 25 inscritos ha sido alcanzado."
    else:
        mensaje_cupos = f"✅ Quedan {LIMITE_CUPOS - total_inscritos} cupos disponibles."

    return render(request, 'index.html', {
        'form': form,
        'mensaje_cupos': mensaje_cupos,
        'tiene_cupos': total_inscritos < LIMITE_CUPOS,
        'total_inscritos': total_inscritos
    })

def exportar_a_excel(request):
    """Genera y descarga un archivo de Excel con los datos de todas las inscripciones."""
    inscripciones = Inscripcion.objects.all().order_by('id')

    output = io.BytesIO()
    workbook = Workbook()
    sheet = workbook.active
    
    # Define los encabezados de las columnas
    sheet['A1'] = 'Resultado del Registro'
    sheet['B1'] = 'Tipo de Identificación'
    sheet['C1'] = 'Número de Identificación'
    sheet['D1'] = 'Código de la Ficha'
    sheet['E1'] = 'Tipo Población Aspirante'
    sheet['F1'] = 'Código Empresa'
    
    # Ancho de las columnas para que se vean bien
    sheet.column_dimensions['A'].width = 25
    sheet.column_dimensions['B'].width = 25
    sheet.column_dimensions['C'].width = 25
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 30
    sheet.column_dimensions['F'].width = 20
    
    # Llena los datos en las filas correspondientes
    row_num = 2
    for inscripcion in inscripciones:
        sheet[f'B{row_num}'] = inscripcion.tipo_identificacion
        sheet[f'C{row_num}'] = inscripcion.numero_identificacion
        sheet[f'E{row_num}'] = inscripcion.tipo_poblacion_aspirante
        row_num += 1

    workbook.save(output)
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="inscripciones.xlsx"'
    
    return response

def exportar_datos_personales(request):
    inscripciones = Inscripcion.objects.all().order_by('id')
    output = io.BytesIO()
    workbook = Workbook()
    sheet = workbook.active

    # Encabezados
    sheet['A1'] = 'Nombre'
    sheet['B1'] = 'Apellido'
    sheet['C1'] = 'Celular'

    # Ancho de columnas
    sheet.column_dimensions['A'].width = 25
    sheet.column_dimensions['B'].width = 25
    sheet.column_dimensions['C'].width = 20

    # Datos
    row_num = 2
    for inscripcion in inscripciones:
        sheet[f'A{row_num}'] = inscripcion.nombre
        sheet[f'B{row_num}'] = inscripcion.apellido
        sheet[f'C{row_num}'] = inscripcion.celular
        row_num += 1

    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="datos_personales.xlsx"'

    return response
from .forms import InscripcionForm
from .models import Inscripcion

def index(request):
    LIMITE_CUPOS = 25
    total_inscritos = Inscripcion.objects.count()

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if total_inscritos >= LIMITE_CUPOS:
            mensaje_cupos = "❌ No existen cupos disponibles para este curso. El límite de 25 inscritos ha sido alcanzado."
        elif form.is_valid():
            form.save()
            return redirect('inscripciones:index')
    else:
        form = InscripcionForm()
        mensaje_cupos = f"✅ Quedan {LIMITE_CUPOS - total_inscritos} cupos disponibles." if total_inscritos < LIMITE_CUPOS else "❌ No existen cupos disponibles para este curso."

    return render(request, 'index.html', {
        'form': form,
        'mensaje_cupos': mensaje_cupos,
        'total_inscritos': total_inscritos,
        'css_file': 'css/formulario.css',
        
        # 'js_file': 'solicitudes/js/solicitudes.js',
    })

from django.contrib import messages
from inscripciones.models import Inscripcion

def detalle_inscripcion(request, pk):
    try:
        inscripcion = Inscripcion.objects.get(pk=pk)
    except Inscripcion.DoesNotExist:
        messages.error(request, f"No se encontró la inscripción con ID {pk}.")
        return redirect('inscripciones:index')  # Asegúrate de que 'index' esté definido en tus URLs

    return render(request, 'index', {
        'inscripcion': inscripcion
    })