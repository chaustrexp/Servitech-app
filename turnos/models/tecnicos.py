from django.db import models
from django.conf import settings


class PerfilTecnico(models.Model):
    """
    Perfil extendido de un técnico: nivel de competencia y dispositivos
    que puede atender. Vinculado 1-a-1 con Usuario (rol=TECNICO).
    """

    class Nivel(models.IntegerChoices):
        NIVEL_1 = 1, 'Nivel 1 — Mantenimiento básico, formateo y repuestos modulares'
        NIVEL_2 = 2, 'Nivel 2 — Software avanzado, firmware y reparación de chasis/conectores'
        NIVEL_3 = 3, 'Nivel 3 — Microelectrónica y microsoldadura en placa base'

    class EspecialidadTecnico(models.TextChoices):
        CELULAR = 'tecnico_celular', 'Especialista en Celulares'
        PC = 'tecnico_pc', 'Especialista en PC de mesa'
        LAPTOP = 'tecnico_laptop', 'Especialista en Portátiles/Laptops'
        GENERAL = 'tecnico_general', 'Técnico General (Todos)'

    tecnico = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_tecnico',
        limit_choices_to={'rol': 'TECNICO'},
    )
    nivel = models.IntegerField(
        choices=Nivel.choices,
        default=Nivel.NIVEL_1,
        verbose_name='Nivel de Competencia',
    )
    especialidad = models.CharField(
        max_length=30,
        choices=EspecialidadTecnico.choices,
        default=EspecialidadTecnico.GENERAL,
        verbose_name='Especialidad Técnica',
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones internas',
    )
    en_pausa_manual = models.BooleanField(
        default=False,
        verbose_name='Pausa Manual',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Técnico'
        verbose_name_plural = 'Perfiles de Técnicos'

    def __str__(self):
        return f"{self.tecnico.nombre_completo} — Nivel {self.nivel}"

    # ── Helpers ──────────────────────────────────────────────────────────────

    @property
    def nivel_color(self):
        return {1: 'emerald', 2: 'blue', 3: 'purple'}.get(self.nivel, 'slate')

    @property
    def nivel_label_corto(self):
        return {1: 'N1', 2: 'N2', 3: 'N3'}.get(self.nivel, '?')

    @property
    def dias_laborales_str(self):
        return ",".join(str(h.dia_semana) for h in self.tecnico.horarios.all())

    @property
    def hora_inicio_str(self):
        first = self.tecnico.horarios.first()
        return first.hora_inicio.strftime("%H:%M") if first else "08:00"

    @property
    def hora_fin_str(self):
        first = self.tecnico.horarios.first()
        return first.hora_fin.strftime("%H:%M") if first else "18:00"
