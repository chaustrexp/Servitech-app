import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servitech_project.settings')
django.setup()

from turnos.models import Usuario, Cita, EstadoCita, Servicio
from turnos.models.horarios import HorarioTecnico
from turnos.services.asignacion import asignar_tecnico, NoTechnicianAvailable

def run_test():
    print("--- INICIANDO PRUEBA DE ASIGNACIÓN AUTOMÁTICA ---")
    
    # 1. Crear horarios para todos los técnicos (si no existen)
    # Lunes a Domingo, de 08:00 a 18:00
    tecnicos = Usuario.objects.filter(rol=Usuario.Rol.TECNICO)
    for tec in tecnicos:
        for dia in range(7): # 0 (Lunes) a 6 (Domingo)
            HorarioTecnico.objects.get_or_create(
                tecnico=tec,
                dia_semana=dia,
                defaults={
                    'hora_inicio': time(8, 0),
                    'hora_fin': time(18, 0)
                }
            )
    print(f"Horarios configurados para {tecnicos.count()} técnicos.")

    # 2. Obtener datos básicos
    clientes = Usuario.objects.filter(rol=Usuario.Rol.CLIENTE)[:3]
    if not clientes:
        print("No hay clientes en la BD.")
        return
    
    estado_confirmada = EstadoCita.objects.get(nombre='CONFIRMADA')
    
    # Supongamos que queremos agendar para mañana a las 10:00 AM
    fecha_cita = date.today() + timedelta(days=1)
    hora_cita = time(10, 0)
    hora_fin_cita = time(11, 0)
    
    # Obtener un servicio de Laptop (tipo_dispositivo = 'LAPTOP')
    servicio_laptop = Servicio.objects.filter(tipo_dispositivo='LAPTOP').first()

    print(f"\nIntentando agendar 3 citas simultáneas de LAPTOP para {fecha_cita} a las {hora_cita}:")
    
    # Intentaremos asignar 3 citas de Laptop al mismo tiempo. 
    # El Tec. Laptop y Tec. General deberían repartirse las citas.
    for i in range(3):
        cliente = clientes[i % len(clientes)]
        try:
            tec_asignado = asignar_tecnico(fecha_cita, hora_cita, 'LAPTOP')
            print(f"Cita {i+1}: Se asignó al técnico -> {tec_asignado.nombre_completo} ({tec_asignado.correo})")
            
            # Guardamos la cita para que el siguiente ciclo del bucle "vea" que este técnico ya tiene carga
            Cita.objects.create(
                cliente=cliente,
                tecnico=tec_asignado,
                servicio=servicio_laptop,
                estado=estado_confirmada,
                fecha=fecha_cita,
                hora_inicio=hora_cita,
                hora_fin=hora_fin_cita
            )
        except NoTechnicianAvailable as e:
            print(f"Cita {i+1}: Falló la asignación -> {e}")

if __name__ == '__main__':
    run_test()
