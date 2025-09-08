from django import forms
from .models import Oferta, Lugar, Horario, EmpresaSolicitante, ProgramaFormacion, Dia


#No olvidar modificarlas
class SubirCedulaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['archivo_cedula_pdf']
        labels = {
            'archivo_cedula_pdf': 'Subir archivo de cédulas (PDF)',
        }

class InstructorArchivoForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['archivo_cedula_pdf']
        widgets = {
            'archivo_cedula_pdf': forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
        }

class EstadoComentarioForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['estado', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }

class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ["departamento", "municipio", "corregimientos", "direccion", "ambiente"]
        widgets = {
            "direccion": forms.TextInput(attrs={"placeholder": "Ej: Calle 12 #3-47"}),
        }


class OfertaForm(forms.ModelForm):
    #Ubicación
    lugar= forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Lugar'})
    )

    #Horarios
    hora_inicio = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form__input'})
    )

    hora_fin = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form__input'})
    )

    dias = forms.ModelMultipleChoiceField(
        queryset=Dia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Días de la semana"
    )

    #Datos de la empresa
    empresa_nombre= forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Nombre de la empresa'})
    )
    empresa_nit= forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'NIT'})
    )
    empresa_subsector= forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Subsector económico'})
    )

    programa= forms.ModelChoiceField(
        queryset= ProgramaFormacion.objects.all(),
        required=True,
        label="Curso",
        widget=forms.Select(attrs={'id': 'selector-cursos', 'class': 'form__input'})
    )


    class Meta:
        model = Oferta
        fields = [
            'modalidad_oferta', 'tipo_oferta', 'entorno_geografico',
            'programa', 'cupo', 'empresa_solicitante',
            'programa_especial',
            'fecha_inicio', 'fecha_de_inscripcion',  'archivo',
        ]

        widgets = {
            'modalidad_oferta': forms.Select(),
            'tipo_oferta': forms.Select(),
            'entorno_geografico': forms.Select(),
            'cupo': forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'Cupo', 'min': 1}),
            'programa_especial': forms.Select(),
            'ficha': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ficha'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
            'fecha_de_inscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),

        }

    def clean_horario(self):
        nombre = self.cleaned_data.get('horario')
        if nombre:
            horario_obj, _ = Horario.objects.get_or_create(
                hora_inicio="08:00",
                hora_fin="12:00",
            )
            return horario_obj
        return None

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('hora_inicio')
        fin = cleaned.get('hora_fin')

        if inicio and fin and inicio >= fin:
            self.add_error('hora_fin', 'La hora fin debe ser posterior a la hora inicio.')


        #Empresa
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo_oferta")
        if tipo == "CERRADA":
            if not cleaned_data.get("empresa_nombre"):
                self.add_error("empresa_nombre", "El nombre de la empresa es obligatorio en oferta cerrada.")
            if not cleaned_data.get("empresa_nit"):
                self.add_error("empresa_nit", "El NIT es obligatorio en oferta cerrada.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # HORARIO
        inicio = self.cleaned_data.get('hora_inicio')
        fin = self.cleaned_data.get('hora_fin')
        horario_obj = None
        if inicio and fin:
            horario_obj, _ = Horario.objects.get_or_create(
                hora_inicio=inicio,
                hora_fin=fin,
            )
            instance.horario = horario_obj

        # LUGAR
        instance.lugar = self.cleaned_data.get('lugar')

        # EMPRESA (si oferta cerrada)
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

