from docxtpl import DocxTemplate
import os
from django.conf import settings


def generar_ficha(oferta):

    template_path = os.path.join(settings.BASE_DIR, "templates/plantillas/ficha_caracterizacion.docx")
    doc = DocxTemplate(template_path)

    context = {
        "codigo_programa": oferta.programaformacion.codigo,
        "nombre_programa": oferta.programaformacion.nombre,
        "version_programa": oferta.programaformacion.version,
        "duracion_programa": oferta.programaformacion.duracion,
        "fecha_inicio ": oferta.fecha_inicio,
        "fecha_fin ": oferta.fecha_terminacion,
        "cupo": oferta.cupo,
        "modalidad": oferta.modalidadprograma.nombre,
        "departamento": oferta.lugar.departamento.nombre,
        "municipio": oferta.lugar.municipio.nombre,
        "direccion": oferta.lugar.direccion,
        "nombre_responsable": oferta.usuario.get_full_name(),
        "numero_identificacion": oferta.usuario.numero_identificacion,
        "email": oferta.usuario.email,
        "fecha_creacion": oferta.creado_en.strftime("%d-%m-%Y"),
        "estado": oferta.estado.nombre,
        "empresa": oferta.empresasolicitante.nombre,
        "subsector": oferta.empresasolicitante.subsector_economico,
        "convenio": oferta.convenio,
        "ambiente": f"oferta.lugar.ambiente.nombre oferta.lugar.ambiente.area",
        #dias
        #horario
        "programa_especial": oferta.programaespecial.nombre,
        "inscripcion": oferta.fecha_inicio,
    }

    doc.render(context)

    output_dir = os.path.join(settings.MEDIA_ROOT, "ficha_caracterizacion")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"ficha_caracterizacion_{oferta.id}.docx")

    doc.save(output_path)

    return f"solicitudes/ficha_caracterizacion_{oferta.id}.docx"