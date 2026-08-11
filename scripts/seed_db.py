import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servitech_project.settings')
django.setup()

from turnos.models.citas import EstadoCita
from turnos.models.servicios import Especialidad, Servicio

def seed():
    print("Sembrando estados de citas...")
    estados = [
        ('PENDIENTE', 'La cita fue creada pero aún no ha sido confirmada'),
        ('CONFIRMADA', 'La cita está confirmada'),
        ('RETRASADA', 'El cliente informó que llegará tarde'),
        ('EN_DIAGNOSTICO', 'El técnico está realizando el diagnóstico'),
        ('EN_REPARACION', 'El dispositivo se encuentra en reparación'),
        ('FINALIZADA', 'La atención de la cita terminó'),
        ('CANCELADA', 'La cita fue cancelada'),
        ('NO_SHOW', 'El cliente no asistió a la cita'),
        ('REAGENDADA', 'La cita fue cambiada para otra fecha u hora')
    ]

    for nombre, desc in estados:
        obj, created = EstadoCita.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
        if created:
            print(f"  Estado creado: {nombre}")

    print("Sembrando especialidades...")
    especialidades = [
        ('CELULARES', 'Diagnóstico y reparación de dispositivos celulares'),
        ('LAPTOPS', 'Diagnóstico y reparación de computadores portátiles'),
        ('PC', 'Diagnóstico y reparación de computadores de escritorio'),
        ('SOFTWARE', 'Instalación y configuración de software'),
        ('HARDWARE', 'Reparación y mantenimiento de componentes físicos')
    ]

    especialidad_objs = {}
    for nombre, desc in especialidades:
        obj, created = Especialidad.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
        if created:
            print(f"  Especialidad creada: {nombre}")
        especialidad_objs[nombre] = obj

    print("Sembrando servicios...")
    servicios = [
        ('Diagnóstico de Celular', 'Revisión general del dispositivo celular', 'CELULAR', 30, 10, 'CELULARES'),
        ('Diagnóstico de Laptop', 'Revisión general del computador portátil', 'LAPTOP', 45, 10, 'LAPTOPS'),
        ('Diagnóstico de PC', 'Revisión general del computador de escritorio', 'PC', 45, 10, 'PC'),
        ('Reparación Exprés de Celular', 'Reparación rápida de un dispositivo celular', 'CELULAR', 60, 15, 'CELULARES'),
        ('Asesoría de Software', 'Asesoría para instalación y configuración de software', 'PC', 30, 5, 'SOFTWARE'),
        ('Mantenimiento de Hardware', 'Mantenimiento preventivo de componentes físicos', 'PC', 60, 15, 'HARDWARE')
    ]

    for nombre, desc, disp, dur, buf, esp_name in servicios:
        obj, created = Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': desc,
                'tipo_dispositivo': disp,
                'duracion_minutos': dur,
                'buffer_minutos': buf,
                'especialidad': especialidad_objs[esp_name]
            }
        )
        if created:
            print(f"  Servicio creado: {nombre}")

    print("¡Base de datos sembrada con éxito!")

if __name__ == '__main__':
    seed()
