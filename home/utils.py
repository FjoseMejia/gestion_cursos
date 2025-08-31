from django.urls import reverse

def sidebar_groups(request):
    user = request.user
    grupo_nombre = user.groups.first().name if user.groups.exists() else "Invitado"

    role_links = {
        "SuperAdmin": [
            {
                "category": "Principal",
                "links": [
                    {"url": "#", "icon": "fas fa-chart-bar", "label": "Reportes"},
                ],
            },
            {
                "category": "Gestión",
                "links": [
                    {"url": '#', "icon": "fas fa-users", "label": "Usuarios"},
                    {"url": "#", "icon": "fas fa-book", "label": "Programas de formación"},
                    {"url": "#", "icon": "fas fa-tasks", "label": "Solicitudes"},
                ],
            },
        ],
        "Instructor": [
            {
                "category": "Gestión",
                "links": [
                    {"url": reverse('ofertas:index'), "icon": "fas fa-tasks", "label": "Solicitudes"},
                    {"url": "#", "icon": "fas fa-history", "label": "Histórico"},
                ],
            },
        ],
        # Agrega los demás roles aquí...
    }

    sidebar_menus = role_links.get(grupo_nombre, [])

    return {
        "sidebar_menus": sidebar_menus,
        "grupo_nombre": grupo_nombre,
    }
