from django.shortcuts import render, redirect
from django.views import View
from usuarios.forms import PerfilForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from usuarios.models import Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from usuarios.forms import PerfilForm, InstructorForm  # <-- importa aquí
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


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
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('usuarios:login')
        else:

            return render(request, "registro/index.html", {'form': form})





# Vista para la gestión de instructores -
def list_user_by_area(request):
    area_user= request.user.area.nombre
    instructores_by_area = Perfil.objects.filter(area__nombre=area_user).values(
        'id',  'username', 'first_name', 'email'
    )


@login_required
def instructores(request):
    user = request.user

    if user.groups.filter(name='Coordinador').exists():
        # 🔹 Coordinador → solo instructores de su área
        area_user = user.area.nombre
        titulo = "Agregar rol (Coordinador)"
        mostrar_acciones = True

        instructores = Perfil.objects.filter(
            area__nombre=area_user,
            groups__name='Instructor'
        ).exclude(
            username=user.username
        ).values(
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'numero_identificacion'
        )

    elif user.groups.filter(name='Funcionario').exists():
        # 🔹 Funcionario → todos los instructores
        area_user = "Todas las áreas"
        titulo = "Gestionar Usuarios (Funcionario)"
        mostrar_acciones = False   # 👈 aquí no mostramos botones

        instructores = Perfil.objects.filter(
            groups__name='Instructor'
        ).exclude(
            username=user.username
        ).values(
            'username', 'first_name', 'last_name',
            'email', 'telefono', 'numero_identificacion'
        )

    elif user.is_superuser:
        # 🔹 Superusuario → todos los roles
        area_user = "Todas las áreas y roles"
        titulo = "Panel de Administración (Superusuario)"
        mostrar_acciones = True

        instructores = Perfil.objects.filter(
            groups__name__in=['Coordinador', 'Funcionario', 'Instructor']
        ).exclude(
            username=user.username
        ).values(
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'numero_identificacion',
            'groups__name', 'area__nombre', 'is_active'
        )

    return render(
        request,
        'instructores/instructores.html',
        {
            'titulo': titulo,
            'area': area_user,
            'instructores': instructores,
            'mostrar_acciones': mostrar_acciones,
            'css_file': 'instructores/css/instructores.css',
            'js_file': 'instructores/js/instructores.js',
        }
    )

    
# BOTON NUEVO USUARIO


User = get_user_model()

def crear_instructor(request):
    if request.method == "POST":
        form = InstructorForm(request.POST, user=request.user)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.set_password("123456")
            nuevo.save()

            # asignación de grupo según quien crea
            if request.user.is_superuser:
                grupo = form.cleaned_data.get("grupo")
                if grupo:
                    nuevo.groups.set([grupo])
            elif request.user.groups.filter(name__in=["Coordinador", "Funcionario"]).exists():
                # forzamos Instructor para coordinador/funcionario
                instructor = Group.objects.filter(name__iexact="Instructor").first()
                if instructor:
                    nuevo.groups.set([instructor])
            else:
                nuevo.groups.clear()

            return redirect("usuarios:instructores")
    else:
        form = InstructorForm(user=request.user)


    return render(
        request, 
        "instructores/nuevo_instructor.html",
        {
            "form": form,
            'css_file': 'instructores/css/nuevo_instructor.css',
            'js_file': 'instructores/js/nuevo_instructor.js',
        }
    )



@csrf_exempt  # ⚠️ si usas fetch con CSRF, puedes quitar esto y pasar el token
def activar_instructor(request, id):
    if request.method == "POST":
        instructor = get_object_or_404(Perfil, id=id)
        instructor.is_active = not instructor.is_active
        instructor.save()
        return JsonResponse({
            "success": True,
            "new_status": instructor.is_active
        })
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)
