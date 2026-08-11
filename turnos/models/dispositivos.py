from django.db import models
from django.conf import settings

class Dispositivo(models.Model):
    TIPO_CHOICES = [
        ('CELULAR', 'Celular'),
        ('LAPTOP', 'Laptop / PC'),
        ('TABLET', 'Tablet'),
        ('CONSOLA', 'Consola'),
        ('OTRO', 'Otro'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dispositivos')
    imei_serial = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="IMEI o Número de Serie")
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CELULAR')
    detalles = models.TextField(blank=True, null=True, help_text="Color, capacidad, estado estético...")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['-fecha_registro']

    def __str__(self):
        identificador = f" (S/N: {self.imei_serial})" if self.imei_serial else ""
        return f"{self.marca} {self.modelo}{identificador} - {self.cliente.nombre_completo}"
