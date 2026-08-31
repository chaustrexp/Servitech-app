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

    def save(self, *args, **kwargs):
        # REGLA DE NEGOCIO: Máquina de Estados Estricta
        if self.pk and self.estado:
            old_cita = Cita.objects.get(pk=self.pk)
            if old_cita.estado and old_cita.estado != self.estado:
                old_state = old_cita.estado.nombre
                new_state = self.estado.nombre
                
                # Definir transiciones válidas
                transiciones_validas = {
                    'PENDIENTE': ['CONFIRMADA', 'CANCELADA'],
                    'CONFIRMADA': ['EN_DIAGNOSTICO', 'RETRASADA', 'CANCELADA'],
                    'RETRASADA': ['EN_DIAGNOSTICO', 'CANCELADA'],
                    'EN_DIAGNOSTICO': ['EN_REPARACION', 'CANCELADA'],
                    'EN_REPARACION': ['FINALIZADA'],
                    'CANCELADA': [],
                    'FINALIZADA': []
                }
                
                # Ignorar validación para administradores o si el estado no está en el mapa para no romper el sistema actual
                if old_state in transiciones_validas and new_state not in transiciones_validas[old_state]:
                    from django.core.exceptions import ValidationError
                    raise ValidationError(f"Transición de estado inválida: No puedes pasar de {old_state} a {new_state}.")
                    
        super().save(*args, **kwargs)

class HistorialCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=50, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)


class CitaRepuesto(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='cita_repuestos')
    repuesto = models.ForeignKey('Repuesto', on_delete=models.PROTECT, related_name='cita_repuestos')
    cantidad = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cita', 'repuesto')

    def __str__(self):
        return f"{self.cantidad}x {self.repuesto.nombre} — Cita #{self.cita.id}"

    def save(self, *args, **kwargs):
        # REGLA DE NEGOCIO: Integridad de Inventario (Anti Stock-Negativo)
        if not self.pk: # Solo al crear (asignar un repuesto nuevo)
            if self.repuesto.stock < self.cantidad:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Stock insuficiente. Solo quedan {self.repuesto.stock} unidades de {self.repuesto.nombre}.")
        super().save(*args, **kwargs)
