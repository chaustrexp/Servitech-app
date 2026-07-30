from django.db import models

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

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
