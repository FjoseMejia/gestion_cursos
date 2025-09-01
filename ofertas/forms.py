from django import forms
from .models import Oferta, Lugar, Horario, EmpresaSolicitante


class OfertaForm(forms.ModelForm):
    # Campos manuales
    lugar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Lugar'})
    )

    horario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Horario'})
    )

    # Campos adicionales para empresa solicitante
    empresa_nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Nombre de la empresa'})
    )
    empresa_nit = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'NIT'})
    )
    empresa_subsector = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Subsector económico'})
    )

    class Meta:
        model = Oferta
        fields = [
            'modalidad_oferta', 'tipo_oferta', 'entorno_geografico',
            'programa', 'cupo', 'empresa_solicitante',
            'subsector', 'programa_especial', 'convenio', 'ficha',
            'fecha_inicio', 'fecha_de_inscripcion', 'fecha_terminacion',
        ]

        widgets = {
            'modalidad_oferta': forms.Select(),
            'tipo_oferta': forms.Select(),
            'entorno_geografico': forms.Select(),
            'programa': forms.TextInput(attrs={'id': 'programa-input', 'class': 'form__input', 'placeholder': 'Escribe el curso...'}),
            'cupo': forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'Cupo', 'min': 1}),
            'subsector': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Subsector'}),
            'programa_especial': forms.Select(),
            'convenio': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Convenio'}),
            'ficha': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ficha'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
            'fecha_de_inscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
            'fecha_terminacion': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
        }

    def clean_lugar(self):
        nombre = self.cleaned_data.get('lugar')
        if nombre:
            lugar_obj, _ = Lugar.objects.get_or_create(direccion=nombre, departamento_id=1, municipio_id=1, corregimientos_id=1, ambiente_id=1)
            return lugar_obj
        return None

    def clean_horario(self):
        nombre = self.cleaned_data.get('horario')
        if nombre:
            horario_obj, _ = Horario.objects.get_or_create(
                hora_inicio="08:00",
                hora_fin="12:00",
                jornada_id=1,
                modalidad_id=1
            )
            # ⚠️ Igual que con Lugar, necesitas decidir cómo quieres manejar la creación de Horarios
            return horario_obj
        return None

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo_oferta")
        if tipo == "CERRADA":  # según tus choices
            if not cleaned_data.get("empresa_nombre"):
                self.add_error("empresa_nombre", "El nombre de la empresa es obligatorio en oferta cerrada.")
            if not cleaned_data.get("empresa_nit"):
                self.add_error("empresa_nit", "El NIT es obligatorio en oferta cerrada.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Lugar y Horario
        instance.lugar = self.cleaned_data.get('lugar')
        instance.horario = self.cleaned_data.get('horario')

        # Empresa solicitante si es cerrada
        if self.cleaned_data.get("tipo_oferta") == "CERRADA":
            nombre = self.cleaned_data.get("empresa_nombre")
            nit = self.cleaned_data.get("empresa_nit")
            subsector = self.cleaned_data.get("empresa_subsector")

            if nombre and nit:
                empresa, _ = EmpresaSolicitante.objects.get_or_create(
                    nit=nit,
                    defaults={"nombre": nombre, "subsector_economico": subsector}
                )
                instance.empresa_solicitante = empresa

        if commit:
            instance.save()
        return instance
