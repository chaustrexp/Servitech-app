from django.db import models
from .usuarios import Usuario

class EstadoSistema(models.Model):
    class Estado(models.TextChoices):
        OPERATIVO = 'operativo', 'Operativo'
        MANTENIMIENTO = 'mantenimiento', 'Mantenimiento'
        FALLO = 'fallo', 'Fallo / Interrupción'

    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.OPERATIVO)
    detalle = models.TextField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"


class TicketSoporte(models.Model):
    class Urgencia(models.TextChoices):
        ALTA = 'Alta', 'Alta (Crítica)'
        MEDIA = 'Media', 'Media'
        BAJA = 'Baja', 'Baja'

    class Estado(models.TextChoices):
        ABIERTO = 'abierto', 'Abierto'
        REVISION = 'revision', 'En Revisión'
        RESUELTO = 'resuelto', 'Resuelto'
        CERRADO = 'cerrado', 'Cerrado'

    titulo = models.CharField(max_length=200)
    area = models.CharField(max_length=100) # Ej: Hardware, Sistemas Centrales, etc.
    urgencia = models.CharField(max_length=20, choices=Urgencia.choices, default=Urgencia.MEDIA)
    descripcion = models.TextField()
    
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ABIERTO)
    
    tecnico = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets_soporte_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.titulo}"
