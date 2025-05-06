from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Importar para la vista de la raíz
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Emergencias",
        default_version='v1',
        description="API para reportar y gestionar emergencias dentro del entorno universitario, permitiendo a los estudiantes crear reportes y a los administradores recibir notificaciones y gestionar las incidencias",
        terms_of_service="https://www.ejemplo.com/terminos/",
        contact=openapi.Contact(email="contacto@ejemplo.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Vista para la ruta raíz
def home(request):
    return HttpResponse("¡Bienvenido a la API de Emergencias!")

urlpatterns = [
    # Ruta para la raíz
    path('', home),  # Esta es la nueva ruta para la raíz

    # Ruta para la administración de Django
    path('admin/', admin.site.urls),

    # Rutas para las APIs de usuarios y emergencias
    path('api/usuarios/', include('usuarios.urls')),  # Rutas para la aplicación 'usuarios'
    path('api/emergencias/', include('emergencias.urls')),  # Rutas para la aplicación 'emergencias'

    # Rutas para la autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas para la documentación de la API (Swagger UI)
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),  # Esta es la ruta que buscas
]