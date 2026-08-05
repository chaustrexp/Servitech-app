from django.db import models

class Repuesto(models.Model):
    CATEGORIA_CHOICES = [
        ('PANTALLAS', 'Pantallas / LCD'),
        ('BATERIAS', 'Baterías'),
        ('CONECTORES', 'Conectores'),
        ('CAMARAS', 'Cámaras'),
        ('ADHESIVOS', 'Adhesivos / Químicos'),
        ('MODULOS', 'Módulos Display'),
        ('OTROS', 'Repuestos Generales'),
    ]

    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='OTROS')
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=150, blank=True, null=True, verbose_name='Proveedor')
    imagen = models.ImageField(upload_to='repuestos/', blank=True, null=True, verbose_name='Foto del Repuesto')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.stock} unidades)"

