from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .serializers import UsuarioSerializer
from .models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import UsuarioSerializer
from .permissions import IsAdminUserCustom  # Asegúrate de tener este permiso personalizado
import os  # Para manejar claves de forma segura

# Registrar Usuario
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        # Si el rol es admin, validamos la clave secreta
        if request.data.get('tipo_usuario') == 'admin':
            clave_secreta = request.data.get('clave_admin')
            clave_esperada = os.getenv('ADMIN_SECRET_KEY', 'admin1234')  # Usamos una variable de entorno para la clave
            if clave_secreta != clave_esperada:
                return Response({'error': 'Clave secreta incorrecta para administrador.'}, status=status.HTTP_403_FORBIDDEN)

        # Validación de la contraseña
        password = request.data.get('password')
        try:
            validate_password(password)  # Valida la contraseña según las reglas de Django
        except ValidationError as e:
            return Response({"error": f"Contraseña inválida: {e.messages}"}, status=status.HTTP_400_BAD_REQUEST)

        # Si todo es correcto, se crea el usuario
        return super().create(request, *args, **kwargs)

# Login con usuario o email
class LoginView(APIView):
    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'mensaje': f'Bienvenido {user.username}',
                    'tipo_usuario': user.tipo_usuario
                })
            else:
                return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Usuario o correo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

# Ver, actualizar y eliminar usuarios — solo Admin debería usar (para un usuario específico por ID)
class UsuarioListUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]  # Requiere autenticación y ser admin

    def get_object(self):
        user = self.request.user
        if user.tipo_usuario != 'admin':
            raise PermissionDenied("No tienes permisos para acceder a esta información.")
        return super().get_object()

    def perform_update(self, serializer):
        if 'tipo_usuario' in self.request.data and self.request.data['tipo_usuario'] == 'admin':
            raise PermissionDenied("No puedes cambiar el tipo de usuario a admin.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.tipo_usuario == 'admin' and instance == self.request.user:
            raise PermissionDenied("No puedes eliminar a ti mismo siendo admin.")
        instance.delete()

# Obtener el perfil del usuario logueado
class MiPerfilView(APIView):
    authentication_classes = [authentication.TokenAuthentication] # O la autenticación que estés usando
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# Listar todos los usuarios de tipo estudiante — solo Admin debería usar
class UsuarioEstudianteListView(generics.ListAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]  # Requiere autenticación y ser admin

    def get_queryset(self):
        return Usuario.objects.filter(tipo_usuario='estudiante')