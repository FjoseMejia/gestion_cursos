import os
from django import template

register = template.Library()

@register.filter
def extension(value):
    """Devuelve la extensión del archivo en minúsculas (ej: .pdf, .docx)"""
    try:
        return os.path.splitext(value.name)[1].lower()
    except Exception:
        return ""
