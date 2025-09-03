from django.shortcuts import render, redirect
from django.views import View
from usuarios.forms import PerfilForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from usuarios.models import Perfil

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
# Vista para la gestión de instructores -
def list_user_by_area(request):
    area_user= request.user.area.nombre
    instructores_by_area = Perfil.objects.filter(area__nombre=area_user).values(
        'username', 'first_name', 'email'
    )

    return  render (
        request,
        'instructores.html', 
        {
            'area': area_user ,
            'instructores':instructores_by_area,
            
        }
    )
