from django.db import models
from django.conf import settings
from .servicios import Servicio

class EstadoCita(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas_cliente')
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_tecnico')
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_dispositivo')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoCita, on_delete=models.PROTECT, null=True, blank=True)
    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    minutos_retraso = models.IntegerField(default=0)
    motivo_cancelacion = models.CharField(max_length=255, blank=True, null=True)
    motivo_reagendamiento = models.CharField(max_length=255, blank=True, null=True)
    minutos_adicionales = models.IntegerField(default=0)
    motivo_ajuste = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita #{self.id} - {self.cliente.correo} ({self.fecha})"

class HistorialCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=50, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
