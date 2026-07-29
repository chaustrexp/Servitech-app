from django.contrib import admin
from .models import Especialidad, Servicio, EstadoCita, HorarioTecnico, Cita, HistorialCita, Notificacion

admin.site.register(Especialidad)
admin.site.register(Servicio)
admin.site.register(EstadoCita)
admin.site.register(HorarioTecnico)
admin.site.register(Cita)
admin.site.register(HistorialCita)
admin.site.register(Notificacion)
