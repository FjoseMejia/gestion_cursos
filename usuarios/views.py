from django.shortcuts import render, redirect
from django.views import View
from usuarios.forms import PerfilForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home:index')
        else:
            error = "Usuario o contraseña incorrectos"
            return render(request, "login/index.html", {"error": error})
    return render(request, "login/index.html")

class Registro(View):
    def get(self, request):
        form= PerfilForm()
        return render(request, "registro/index.html", {'form': form})

    def post(self, request):
        form = PerfilForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']

            if '@sena.edu.co' in email:
                grupo, created = Group.objects.get_or_create(name='Instructor')
                user.groups.add(grupo)
            else:
                grupo, created = Group.objects.get_or_create(name='Invitado')
                user.groups.add(grupo)

            return redirect('usuarios:login')
        else:

            return render(request, "registro/index.html", {'form': form})

def recovery_password(request, email):
    return render(request, 'recovery_password.html', {'email': email})

# Vista para la gestión de instructores -
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil
from django.db.models import Q

@login_required
def instructores(request):
    usuario_actual = request.user
    
    # Determinar el queryset según el rol del usuario
    if usuario_actual.is_superuser or usuario_actual.groups.filter(name__in=['Admin', 'Administrador']).exists():
        # Admin o superadmin ve todos los roles
        perfiles = Perfil.objects.all()
        instructores = Perfil.objects.filter(groups__name='Instructor')
        coordinadores = Perfil.objects.filter(groups__name='Coordinador')
        funcionarios = Perfil.objects.filter(groups__name='Funcionario')
    
    elif usuario_actual.groups.filter(name='Coordinador').exists():
        # Coordinador ve solo instructores
        perfiles = Perfil.objects.filter(groups__name='Instructor')
        instructores = perfiles
        coordinadores = Perfil.objects.none()
        funcionarios = Perfil.objects.none()
    
    elif usuario_actual.groups.filter(name='Funcionario').exists():
        # Funcionario ve solo instructores
        perfiles = Perfil.objects.filter(groups__name='Instructor')
        instructores = perfiles
        coordinadores = Perfil.objects.none()
        funcionarios = Perfil.objects.none()
    
    else:
        # Para otros roles (Instructor u otros), solo se ve a sí mismo
        perfiles = Perfil.objects.filter(id=usuario_actual.id)
        instructores = perfiles
        coordinadores = Perfil.objects.none()
        funcionarios = Perfil.objects.none()
    
    # Obtener el nombre del grupo principal del usuario
    grupo_principal = "Invitado"
    if usuario_actual.groups.exists():
        grupo_principal = usuario_actual.groups.first().name
    
    # Contexto para el template
    context = {
        'grupo_nombre': grupo_principal,
        'perfiles': perfiles.select_related('tipo_identificacion', 'area').prefetch_related('groups'),
        'instructores': instructores.select_related('tipo_identificacion', 'area').prefetch_related('groups'),
        'coordinadores': coordinadores.select_related('tipo_identificacion', 'area').prefetch_related('groups'),
        'funcionarios': funcionarios.select_related('tipo_identificacion', 'area').prefetch_related('groups'),
        'total_instructores': perfiles.count(),
        'css_file': 'instructores/css/instructores.css',
        'js_file': 'instructores/js/instructores.js',
    }
    
    return render(request, 'instructores.html', context)