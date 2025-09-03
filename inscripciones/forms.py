from django import forms
from .models import Inscripcion

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'
        widgets = {
            'tipo_identificacion': forms.Select(attrs={
                'class': 'form-control select-identificacion'
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Ej. 1234567890'
            }),
            'tipo_poblacion_aspirante': forms.Select(attrs={
                'class': 'form-control select-identificacion'
            }),
            'fecha_registro': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Juan'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Pérez'
            }),
            'celular': forms.TextInput(attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder': 'Ej. 3001234567'
            }),
        }