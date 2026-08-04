from django.db import models
from django.conf import settings
from .citas import Cita

class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=500)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
