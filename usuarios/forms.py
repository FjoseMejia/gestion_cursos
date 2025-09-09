# usuarios/forms.py
from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class PerfilForm(UserCreationForm):
    class Meta:
        model = Perfil
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'tipo_identificacion',
            'numero_identificacion',
            'area',
            'password1',
            'password2',
        ]

        labels = {
            'username': 'Usuario',
            'first_name': 'Nombres',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',

        }

        widgets = {
            'telefono': forms.NumberInput(attrs={'class': 'form__input', 'placeholder': 'Teléfono'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Número de identificación'}),
            'tipo_identificacion': forms.Select(),
            'area': forms.Select(),
            'email': forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'Correo electrónico'}),
        }
# modi

User = get_user_model()

class InstructorForm(forms.ModelForm):
    # campo personalizado (singular) — así evitamos el ManyToMany por defecto
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        label="Grupo",
        empty_label="---------"
    )

    class Meta:
        model = User
        # IMPORTANTE: no incluir "groups" aquí
        fields = [
            "username", "first_name", "last_name", "email",
            "telefono", "numero_identificacion", "area", "is_active"
        ]

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # si superuser -> ve todos los grupos
        if request_user and request_user.is_superuser:
            self.fields["grupo"].queryset = Group.objects.all()

        # si coordinador o funcionario -> solo Instructor
        elif request_user and request_user.groups.filter(name__in=["Coordinador", "Funcionario"]).exists():
            qs = Group.objects.filter(name__iexact="Instructor")
            self.fields["grupo"].queryset = qs
            # poner el initial para que se vea seleccionado si solo hay uno
            if qs.exists():
                self.fields["grupo"].initial = qs.first()

        # otros -> sin opciones
        else:
            self.fields["grupo"].queryset = Group.objects.none()
