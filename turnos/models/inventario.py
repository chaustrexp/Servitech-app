from django.db import models
from django.conf import settings
from .repuestos import Repuesto
from .citas import Cita

class Inventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]

    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='inventarios')
    cantidad = models.IntegerField(default=1)
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES, default='ENTRADA')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name='repuestos_usados')
    motivo = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"{self.tipo} - {self.cantidad}x {self.repuesto.nombre} ({self.fecha.strftime('%d/%m/%Y')})"
