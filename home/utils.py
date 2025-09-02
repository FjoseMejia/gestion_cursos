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
                    {"url": "#", "icon": "fas fa-tasks", "label": "Ofertas"},
                ],
            },
        ],
        "Instructor": [
            {
                "category": "Gestión",
                "links": [
                    {"url": reverse('ofertas:index'), "icon": "fas fa-tasks", "label": "Ofertas"},
                    {"url": "#", "icon": "fas fa-history", "label": "Histórico"},
                ],
            },
        ],
        "Funcionario": [
            {
                "category": "Principal",
                "links": [
                    {
                        "url": reverse('ofertas:fichas'),  # debes crear esta vista si no existe
                        "icon": "fas fa-chart-bar",
                        "label": "Reportes ",
                    },
                ],
            },
            {
                "category": "Gestión",
                "links": [
                    {
                        "url": reverse('ofertas:solicitudes_list'),  # Cursos: listar, CRUD sin eliminar
                        "icon": "fas fa-book",
                        "label": "Cursos",
                    },
                    {
                        "url": reverse('ofertas:solicitudes_list'),  # Visualización de documentos
                        "icon": "fas fa-file-excel",
                        "label": "Solicitudes",
                    },
                ],
            },
        ],
    }
            
    sidebar_menus = role_links.get(grupo_nombre, [])

    return {
        "sidebar_menus": sidebar_menus,
        "grupo_nombre": grupo_nombre,
    }
