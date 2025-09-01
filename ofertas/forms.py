from django import forms
from .models import Oferta, Lugar, Horario


class OfertaForm(forms.ModelForm):

    lugar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Lugar'})
    )
    horario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Horario'})
    )

    class Meta:
        model = Oferta
        fields = [
            'modalidad_oferta', 'tipo_oferta', 'entorno_geografico',
            'programa', 'lugar', 'horario', 'cupo', 'empresa_solicitante',
            'subsector', 'programa_especial', 'convenio', 'ficha',
            'fecha_inicio', 'fecha_de_inscripcion', 'fecha_terminacion',
        ]
        widgets = {
            'modalidad_oferta': forms.Select(),
            'tipo_oferta': forms.Select(),
            'entorno_geografico': forms.Select(),
            'programa': forms.Select(),
            'cupo': forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'Cupo', 'min': 1}),
            'empresa_solicitante': forms.Select(),
            'subsector': forms.Select(),
            'programa_especial': forms.Select(),
            'convenio': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Convenio'}),
            'ficha': forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'Ficha'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
            'fecha_de_inscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
            'fecha_terminacion': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
        }

    def clean_lugar(self):
        nombre = self.cleaned_data.get('lugar')
        if nombre:
            lugar_obj, _ = Lugar.objects.get_or_create(nombre=nombre)
            return lugar_obj
        return None

    def clean_horario(self):
        nombre = self.cleaned_data.get('horario')
        if nombre:
            horario_obj, _ = Horario.objects.get_or_create(nombre=nombre)
            return horario_obj
        return None

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.lugar = self.cleaned_data.get('lugar')
        instance.horario = self.cleaned_data.get('horario')
        if commit:
            instance.save()
        return instance
