# Las tablas SQL que definimos

from django.db import models
from django.contrib.auth.models import User

# 1. ESPECIALIDAD
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# 2. SERVICIO
class Servicio(models.Model):
    TIPO_DISPOSITIVO_CHOICES = [
        ('CELULAR', 'Celular'),
        ('LAPTOP', 'Laptop'),
        ('PC', 'PC'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    tipo_dispositivo = models.CharField(max_length=30, choices=TIPO_DISPOSITIVO_CHOICES)
    duracion_minutos = models.IntegerField()
    buffer_minutos = models.IntegerField(default=0)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='servicios')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_dispositivo})"


# 3. ESTADO CITA
class EstadoCita(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre


# 4. HORARIO TÉCNICO
class HorarioTecnico(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField() # 1 a 7
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Día {self.dia_semana}: {self.hora_inicio} - {self.hora_fin}"


# 5. CITA / TURNO (Tabla Principal)
class Cita(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas_cliente')
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_tecnico')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoCita, on_delete=models.PROTECT, default=1)
    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    # Contingencias y Retrasos
    minutos_retraso = models.IntegerField(default=0)
    motivo_cancelacion = models.CharField(max_length=255, blank=True, null=True)
    motivo_reagendamiento = models.CharField(max_length=255, blank=True, null=True)
    minutos_adicionales = models.IntegerField(default=0)
    motivo_ajuste = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita #{self.id} - {self.cliente.username} ({self.fecha})"


# 6. HISTORIAL CITA
class HistorialCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=50, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)


# 7. NOTIFICACIÓN
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=500)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)