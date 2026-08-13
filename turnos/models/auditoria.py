from django.db import models


class AuditoriaLog(models.Model):
    """
    Tabla central de auditoría. Los triggers de PostgreSQL escriben aquí
    ante cualquier INSERT, UPDATE o DELETE en las tablas monitoreadas.
    """

    class Tabla(models.TextChoices):
        CITAS     = 'citas',     'Citas'
        CLIENTES  = 'clientes',  'Clientes'
        PERSONAS  = 'personas',  'Personas'
        SESIONES  = 'sesiones',  'Sesiones'

    class Operacion(models.TextChoices):
        INSERT = 'INSERT', 'Inserción'
        UPDATE = 'UPDATE', 'Actualización'
        DELETE = 'DELETE', 'Eliminación'

    tabla       = models.CharField(max_length=50, choices=Tabla.choices)
    operacion   = models.CharField(max_length=10, choices=Operacion.choices)
    registro_id = models.BigIntegerField(null=True, blank=True, help_text="PK del registro afectado")
    datos_antes = models.JSONField(null=True, blank=True, help_text="Valores anteriores (UPDATE/DELETE)")
    datos_despues = models.JSONField(null=True, blank=True, help_text="Valores nuevos (INSERT/UPDATE)")
    usuario_db  = models.CharField(max_length=150, blank=True, null=True, help_text="Usuario de base de datos")
    ip_cliente  = models.GenericIPAddressField(null=True, blank=True)
    fecha       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table   = 'auditoria_log'
        ordering   = ['-fecha']
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'

    def __str__(self):
        return f"[{self.fecha:%Y-%m-%d %H:%M}] {self.operacion} en {self.tabla} (id={self.registro_id})"
