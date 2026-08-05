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

    class Dispositivo(models.TextChoices):
        CELULAR  = 'CELULAR',  'Celular'
        PC_MESA  = 'PC_MESA',  'PC de Mesa'
        PORTATIL = 'PORTATIL', 'Portátil'

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
    # Especialidades: guardadas como string con separador ','
    # Ej: "CELULAR,PORTATIL"
    especialidades = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Dispositivos que atiende',
        help_text='Lista separada por comas: CELULAR, PC_MESA, PORTATIL',
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones internas',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Técnico'
        verbose_name_plural = 'Perfiles de Técnicos'

    def __str__(self):
        return f"{self.tecnico.nombre_completo} — Nivel {self.nivel}"

    # ── Helpers ──────────────────────────────────────────────────────────────
    def get_especialidades_list(self):
        """Devuelve las especialidades como lista limpia."""
        return [e.strip() for e in self.especialidades.split(',') if e.strip()]

    def set_especialidades_list(self, lista):
        """Recibe una lista y la guarda como string separado por comas."""
        self.especialidades = ','.join(lista)

    def get_especialidades_display(self):
        """Devuelve etiquetas legibles de las especialidades."""
        mapa = dict(PerfilTecnico.Dispositivo.choices)
        return [mapa.get(e, e) for e in self.get_especialidades_list()]

    @property
    def nivel_color(self):
        return {1: 'emerald', 2: 'blue', 3: 'purple'}.get(self.nivel, 'slate')

    @property
    def nivel_label_corto(self):
        return {1: 'N1', 2: 'N2', 3: 'N3'}.get(self.nivel, '?')
