from django.urls import path
from .views import CrearEmergenciaView, ListarEmergenciasView, EliminarEmergenciaView

urlpatterns = [
    path('lista/', ListarEmergenciasView.as_view(), name='listar_emergencias'),
    path('crear/', CrearEmergenciaView.as_view(), name='crear_emergencia'),
    path('eliminar/<int:pk>/eliminar/', EliminarEmergenciaView.as_view(), name='eliminar_emergencia'),
]
