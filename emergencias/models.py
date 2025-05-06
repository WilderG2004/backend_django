from django.db import models
from usuarios.models import Usuario

class Emergencia(models.Model):
    tipo = models.CharField(max_length=255, blank=True, null=True)  # Puede quedar vacío
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha automática
    piso = models.IntegerField(blank=True, null=True)  # Piso puede quedar vacío
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)  # Puede quedar vacío

    def __str__(self):  # Corrige la indentación aquí
        if self.usuario:
            return f"{self.tipo} reportada por {self.usuario.nombre}"
        return f"{self.tipo} reportada por usuario desconocido"