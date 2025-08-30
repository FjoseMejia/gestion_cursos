from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def index(request):
    user= request.user
    grupo = user.groups.first()
    grupo_nombre = grupo.name if grupo else "Invitado"
    return render(request, 'ofertas.html', {'grupo_nombre': grupo_nombre})