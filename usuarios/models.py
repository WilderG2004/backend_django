from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=255, blank=True, null=True)  # Se permite vacío
    correo = models.EmailField(unique=True, blank=True, null=True)  # Se permite vacío
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Se permite vacío
    contrasenia = models.CharField(max_length=128, blank=True, null=True)  # Puede quedar vacío
    tipo_usuario = models.CharField(max_length=50, blank=True, null=True)  # Puede quedar vacío

    def save(self, *args, **kwargs):
        if self.telefono and not self.telefono.startswith('+57'):
            self.telefono = '+57' + self.telefono
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre