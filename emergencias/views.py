from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Emergencia
from .serializers import EmergenciaSerializer
from rest_framework import permissions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.generics import ListAPIView
from rest_framework import serializers



# Vista para Listar Emergencias (GET)
class ListarEmergenciasView(generics.ListAPIView):
    queryset = Emergencia.objects.all()
    serializer_class = EmergenciaSerializer

# Permiso personalizado para verificar si el usuario es administrador
class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'admin'

class CrearEmergenciaView(generics.CreateAPIView):
    serializer_class = EmergenciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        emergencia = serializer.save(usuario=self.request.user)
        
        channel_layer = get_channel_layer()
        # Asegúrate que el nombre del grupo sea coherente, aquí lo tienes como "emergencias"
        async_to_sync(channel_layer.group_send)(
            "emergencias",
            {
                "type": "enviar_emergencia", # Debe coincidir con el método en el Consumer
                "data": {
                    "usuario": emergencia.usuario.nombre,
                    "tipo": emergencia.tipo,
                    "piso": emergencia.piso,
                    "fecha": str(emergencia.fecha) # Asegúrate de que fecha sea serializable
                }
            }
        )

            

# Vista para Eliminar Emergencia (DELETE)
class EliminarEmergenciaView(generics.DestroyAPIView):
    queryset = Emergencia.objects.all()
    serializer_class = EmergenciaSerializer
    permission_classes = [IsAdminUserCustom]  # Solo los administradores pueden eliminar emergencias

    def delete(self, request, *args, **kwargs):
        # Asegura que el admin está intentando eliminar una emergencia
        if not request.user.tipo_usuario == 'admin':
            return Response(
                {"detail": "No tienes permisos para eliminar esta emergencia."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)