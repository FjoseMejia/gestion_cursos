# inscripciones/forms.py
from django import forms
from .models import Inscripcion

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['tipo_identificacion', 'numero_identificacion', 'tipo_poblacion_aspirante']
        labels = {
            'tipo_identificacion': 'Tipo de Identificación',
            'numero_identificacion': 'Número de Identificación',
            'tipo_poblacion_aspirante': 'Tipo Población Aspirante',
        }