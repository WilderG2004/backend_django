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
        try:
            emergencia = serializer.save(usuario=self.request.user)
            # No es necesario recargar la emergencia si el serializer maneja la fecha correctamente

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "emergencias",
                {
                    "type": "enviar_emergencia",
                    "data": {
                        "usuario": emergencia.usuario.nombre,  # Usa emergencia.usuario.nombre aquí
                        "tipo": emergencia.tipo,
                        "piso": emergencia.piso,
                        "fecha": str(emergencia.fecha)
                    }
                }
            )

            # Serializa la emergencia recién creada para la respuesta de la API
            response_serializer = EmergenciaSerializer(emergencia)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

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