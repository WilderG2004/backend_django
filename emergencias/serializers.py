from rest_framework import serializers
from .models import Emergencia
from usuarios.models import Usuario  

class EmergenciaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Emergencia
        fields = ['id', 'usuario_nombre', 'tipo', 'piso', 'fecha']
        read_only_fields = ['id', 'usuario_nombre', 'fecha']