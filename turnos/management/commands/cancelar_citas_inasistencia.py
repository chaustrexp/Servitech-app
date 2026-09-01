from django.core.management.base import BaseCommand
from turnos.services.cancelacion_automatica import cancelar_citas_vencidas

class Command(BaseCommand):
    help = 'Cancela automáticamente citas en las que el cliente no se presentó tras 15 minutos de tolerancia.'

    def handle(self, *args, **options):
        canceladas = cancelar_citas_vencidas()
        count = len(canceladas)
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Se cancelaron {count} cita(s) por inasistencia.'))
            for c in canceladas:
                self.stdout.write(f' - Cita #{c.pk}: {c.cliente.nombre_completo} ({c.fecha} {c.hora_inicio})')
        else:
            self.stdout.write(self.style.SUCCESS('No se encontraron citas vencidas por inasistencia.'))
