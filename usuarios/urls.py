from django.urls import path
from .views import RegistroUsuarioView, LoginView, UsuarioListUpdateDelete, MiPerfilView, UsuarioEstudianteListView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:pk>/', UsuarioListUpdateDelete.as_view(), name='usuario_crud'),
    path('mi-perfil/', MiPerfilView.as_view(), name='mi_perfil'), 
    path('', UsuarioEstudianteListView.as_view(), name='listar_estudiantes'),
]
