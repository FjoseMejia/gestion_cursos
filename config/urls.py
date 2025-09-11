from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('usuarios.urls_reset')),
    path('usuarios/', include('usuarios.urls')),
    path('ofertas/', include('ofertas.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path("chaining/", include("smart_selects.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)