import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servitech_project.settings')
django.setup()

from turnos.models import Cita, EstadoCita, Servicio, Especialidad, Usuario

def run_seed():
    print("--- Sembrando Citas de Prueba en PostgreSQL (turnos_cita) ---")
    
    # 1. Asegurar Estados de Cita
    estados_def = [
        ('PENDIENTE', 'Cita creada pero pendiente de confirmación/atención'),
        ('CONFIRMADA', 'Cita confirmada'),
        ('RETRASADA', 'Cliente en camino con retraso notificado'),
        ('EN_DIAGNOSTICO', 'El técnico realiza el diagnóstico preliminar'),
        ('EN_REPARACION', 'El equipo está en proceso de reparación'),
        ('FINALIZADA', 'Servicio completado satisfactoriamente'),
        ('CANCELADA', 'Cita cancelada por cliente o sistema'),
    ]
    estados = {}
    for nombre, desc in estados_def:
        obj, _ = EstadoCita.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
        estados[nombre] = obj

    # 2. Asegurar Especialidades y Servicios
    esp_gen, _ = Especialidad.objects.get_or_create(nombre='GENERAL', defaults={'descripcion': 'General'})
    esp_cel, _ = Especialidad.objects.get_or_create(nombre='CELULARES', defaults={'descripcion': 'Móviles y Tablets'})
    esp_lap, _ = Especialidad.objects.get_or_create(nombre='LAPTOPS', defaults={'descripcion': 'Computadores Portátiles'})

    serv_mac, _ = Servicio.objects.get_or_create(
        nombre='Reparación de Pantalla Laptop',
        defaults={'descripcion': 'Sustitución de pantalla parpadeante o rota', 'duracion_minutos': 90, 'tipo_dispositivo': 'LAPTOP', 'especialidad': esp_lap}
    )
    serv_cel, _ = Servicio.objects.get_or_create(
        nombre='Cambio de Pantalla OLED',
        defaults={'descripcion': 'Reemplazo de display completo', 'duracion_minutos': 60, 'tipo_dispositivo': 'CELULAR', 'especialidad': esp_cel}
    )
    serv_diag, _ = Servicio.objects.get_or_create(
        nombre='Diagnóstico de Rendimiento',
        defaults={'descripcion': 'Evaluación general y pruebas térmicas/software', 'duracion_minutos': 60, 'tipo_dispositivo': 'PC', 'especialidad': esp_gen}
    )
    serv_bater, _ = Servicio.objects.get_or_create(
        nombre='Cambio de Batería y Mantenimiento',
        defaults={'descripcion': 'Mantenimiento interno y reemplazo de batería', 'duracion_minutos': 45, 'tipo_dispositivo': 'CELULAR', 'especialidad': esp_cel}
    )

    # 3. Crear o recuperar Clientes de Prueba
    clientes_data = [
        ("Ana Torres", "ana.torres@gmail.com", "3001234567"),
        ("Carlos Mendoza", "carlos.mendoza@gmail.com", "3119876543"),
        ("María García", "maria.garcia@gmail.com", "3204567890"),
        ("Roberto López", "roberto.lopez@gmail.com", "3156543210"),
        ("Sofía Ramírez", "sofia.ramirez@gmail.com", "3187654321"),
    ]
    clientes = []
    for nombre, correo, tel in clientes_data:
        usr, created = Usuario.objects.get_or_create(
            correo=correo,
            defaults={
                'nombre_completo': nombre,
                'telefono': tel,
                'rol': Usuario.Rol.CLIENTE,
                'username': correo
            }
        )
        if created:
            usr.set_password('123456')
            usr.save()
        clientes.append(usr)

    # 4. Crear Citas de Prueba
    hoy = date.today()
    manana = hoy + timedelta(days=1)

    citas_test = [
        {
            'cliente': clientes[0],
            'servicio': serv_mac,
            'estado': estados['PENDIENTE'],
            'fecha': hoy,
            'hora_inicio': time(10, 0),
            'hora_fin': time(11, 30),
            'observaciones': 'Dispositivo: MacBook Pro M2 | Falla: Pantalla parpadeante en brillo alto'
        },
        {
            'cliente': clientes[1],
            'servicio': serv_cel,
            'estado': estados['PENDIENTE'],
            'fecha': hoy,
            'hora_inicio': time(13, 0),
            'hora_fin': time(14, 0),
            'observaciones': 'Dispositivo: Samsung Galaxy S24 | Falla: Cambio de pantalla por caída'
        },
        {
            'cliente': clientes[2],
            'servicio': serv_diag,
            'estado': estados['PENDIENTE'],
            'fecha': manana,
            'hora_inicio': time(9, 30),
            'hora_fin': time(10, 30),
            'observaciones': 'Dispositivo: Dell XPS 15 | Falla: Diagnóstico de rendimiento por sobrecalentamiento'
        },
        {
            'cliente': clientes[3],
            'servicio': serv_bater,
            'estado': estados['PENDIENTE'],
            'fecha': manana,
            'hora_inicio': time(11, 0),
            'hora_fin': time(12, 0),
            'observaciones': 'Dispositivo: iPhone 14 Pro | Falla: La batería se descarga rápido'
        },
        {
            'cliente': clientes[4],
            'servicio': serv_diag,
            'estado': estados['EN_DIAGNOSTICO'],
            'fecha': hoy,
            'hora_inicio': time(8, 0),
            'hora_fin': time(9, 0),
            'observaciones': 'Dispositivo: HP Spectre x360 | Falla: El teclado no responde'
        },
        {
            'cliente': clientes[0],
            'servicio': serv_mac,
            'estado': estados['FINALIZADA'],
            'fecha': hoy - timedelta(days=1),
            'hora_inicio': time(15, 0),
            'hora_fin': time(16, 30),
            'observaciones': 'Dispositivo: MacBook Air M1 | Servicio de limpieza interna finalizado'
        },
        {
            'cliente': clientes[1],
            'servicio': serv_cel,
            'estado': estados['RETRASADA'],
            'fecha': hoy,
            'hora_inicio': time(16, 0),
            'hora_fin': time(17, 0),
            'minutos_retraso': 15,
            'observaciones': 'Dispositivo: Xiaomi 13 Pro | El cliente avisó que llegará 15 mins tarde'
        }
    ]

    count = 0
    for c_data in citas_test:
        cita, created = Cita.objects.get_or_create(
            cliente=c_data['cliente'],
            fecha=c_data['fecha'],
            hora_inicio=c_data['hora_inicio'],
            defaults=c_data
        )
        if created:
            count += 1
            print(f"  -> Cita creada para {cita.cliente.nombre_completo} ({cita.fecha} {cita.hora_inicio})")

    print(f"\n¡Éxito! Se han registrado {count} nuevas citas de prueba en la tabla 'turnos_cita' de PostgreSQL.")
    print(f"Total citas actuales en la base de datos: {Cita.objects.count()}")

if __name__ == '__main__':
    run_seed()
