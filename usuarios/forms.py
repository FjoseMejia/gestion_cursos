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
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class InstructorForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.none(),  # por defecto vacío
        required=True,
        label="Grupo"
    )

    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email",
            "telefono", "numero_identificacion", "area", "is_active",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # capturamos usuario logueado
        super().__init__(*args, **kwargs)

        if user:
            if user.is_superuser:
                # 🔹 Superusuario → todos los grupos
                self.fields["grupo"].queryset = Group.objects.all()
            elif user.groups.filter(name__in=["Coordinador", "Funcionario"]).exists():
                # 🔹 Coordinador o Funcionario → solo Instructor
                self.fields["grupo"].queryset = Group.objects.filter(name="Instructor")
            else:
                # 🔹 Otros usuarios → no pueden asignar grupo
                self.fields["grupo"].queryset = Group.objects.none()
