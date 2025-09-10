from django.urls import reverse

def sidebar_groups(request):
    user = request.user
    grupo_nombre = user.groups.first().name if user.groups.exists() else "SuperAdmin"

    role_links = {
        "SuperAdmin": [
            {
                "category": "Francisco",
                "links": [
                    {"url": "#", "icon": "fas fa-chart-bar", "label": "Reportes"},
                ],
            },
            {
                "category": "Gestión",
                "links": [
                    {"url": reverse('usuarios:instructores'), "icon": "fas fa-users", "label": "Usuarios"},
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
                "category": "Gestión",
                "links": [
                    {"url": reverse('ofertas:solicitudes'), "icon": "fas fa-inbox", "label": "Solicitudes"},
                    {"url": reverse('ofertas:reportes'), "icon": "fas fa-chart-line", "label": "Reportes"},
                    {"url": "#", "icon": "fas fa-book-open", "label": "Programas"},
                    {"url":  reverse('usuarios:instructores'), "icon": "fas fa-chalkboard-teacher", "label": "Instructores"},

                ]
            }
        ],
        "Coordinador": [
            {
                "category": "Gestión",
                "links": [
                    {"url": reverse('ofertas:solicitudes'), "icon": "fas fa-inbox", "label": "Solicitudes"},
                    {"url": "#", "icon": "fas fa-inbox", "label": "Solicitudes"},
                    {"url":  reverse('usuarios:instructores'), "icon": "fas fa-chalkboard-teacher", "label": "Instructores"},
                ]
            }
        ],
    }
            
    sidebar_menus = role_links.get(grupo_nombre, [])

    return {
        "sidebar_menus": sidebar_menus,
        "grupo_nombre": grupo_nombre,
    }
