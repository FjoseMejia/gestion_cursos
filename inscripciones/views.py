# inscripciones/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InscripcionForm
from .models import Inscripcion
from openpyxl import Workbook
import io

def inscripcion_formulario(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            # La corrección está aquí: redirigimos al mismo formulario
            return redirect('index')
    else:
        form = InscripcionForm()
    
    # La corrección está aquí: siempre renderizamos la plantilla con el formulario
    return render(request, 'index.html', {'form': form})

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
    """Genera y descarga un archivo de Excel con nombre, apellido y celular."""
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