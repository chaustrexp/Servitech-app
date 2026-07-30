from django.db import models
from django.conf import settings

class HorarioTecnico(models.Model):
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Día {self.dia_semana}: {self.hora_inicio} - {self.hora_fin}"
