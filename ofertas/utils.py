from docxtpl import DocxTemplate
import os
from django.conf import settings


def generar_ficha(oferta):

    template_path = os.path.join(settings.BASE_DIR, "templates/plantillas/ficha_de_caracterizacion.docx")
    doc = DocxTemplate(template_path)

    context = {
        "codigo_programa": safe_attr(oferta.programa, "codigo"),
        "nombre_programa": safe_attr(oferta.programa, "nombre"),
        "version_programa": safe_attr(oferta.programa, "version"),
        "duracion_programa": safe_attr(oferta.programa, "duracion"),
        "fecha_inicio": oferta.fecha_inicio,
        "fecha_fin": oferta.fecha_terminacion,
        "cupo": oferta.cupo,
        "modalidad": safe_attr(oferta.modalidad_programa, "nombre"),
        "departamento": safe_attr(safe_attr(oferta.lugar, "departamento"), "nombre"),
        "municipio": safe_attr(safe_attr(oferta.lugar, "municipio"), "nombre"),
        "direccion": safe_attr(oferta.lugar, "direccion"),
        "nombre_responsable": safe_attr(oferta.usuario, "get_full_name")(),
        "numero_identificacion": safe_attr(oferta.usuario, "numero_identificacion"),
        "email": safe_attr(oferta.usuario, "email"),
        "fecha_creacion": oferta.creado_en.strftime("%d-%m-%Y") if oferta.creado_en else "",
        "estado": safe_attr(oferta.estado, "nombre"),
        "empresa": safe_attr(oferta.empresa_solicitante, "nombre"),
        "subsector": safe_attr(oferta.empresa_solicitante, "subsector_economico"),
        #"convenio": oferta.empresa_solicitante.convenio or "",
        "ambiente": f"{safe_attr(safe_attr(oferta.lugar, 'ambiente'), 'nombre')} {safe_attr(safe_attr(oferta.lugar, 'ambiente'), 'area')}",
        "programa_especial": safe_attr(oferta.programa_especial, "nombre"),
        "inscripcion": oferta.fecha_inicio,
    }

    doc.render(context)

    output_dir = os.path.join(settings.MEDIA_ROOT, "ficha_caracterizacion")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"ficha_caracterizacion_{oferta.id}.docx")

    doc.save(output_path)

    return f"solicitudes/ficha_caracterizacion_{oferta.id}.docx"

def safe_attr(obj, attr, default=""):
    if obj is None:
        return default
    return getattr(obj, attr, default)
