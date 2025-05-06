from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Usuario.objects.all())]
    )
    nombre = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, required=False)  # Contraseña opcional en la actualización
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Usuario.objects.all())],
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'telefono', 'tipo_usuario', 'nombre']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        nombre = validated_data.pop('nombre')
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        user.nombre = nombre
        user.save()
        return user

    def update(self, instance, validated_data):
        # Actualiza los campos que se proporcionan en la petición
        instance.username = validated_data.get('username', instance.username)  # Permitir actualizar el username
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.email = validated_data.get('email', instance.email)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.tipo_usuario = validated_data.get('tipo_usuario', instance.tipo_usuario)

        # Solo actualiza la contraseña si se proporciona una nueva
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])
        instance.save()
        return instance