from django.db import models

class Repuesto(models.Model):
    CATEGORIA_CHOICES = [
        ('PANTALLAS', 'Pantallas'),
        ('BATERIAS', 'Baterías'),
        ('CONECTORES', 'Conectores'),
        ('CAMARAS', 'Cámaras'),
        ('OTROS', 'Otros'),
    ]

    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='OTROS')
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.stock} unidades)"
