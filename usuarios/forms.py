# usuarios/forms.py
from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm

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
