import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servitech_project.settings')
django.setup()

from turnos.models import Usuario, EstadoCita, Especialidad, Servicio, Cita
from turnos.models.tecnicos import PerfilTecnico

def run():
    print("Inyectando datos iniciales de ServiTech...")

    # 1. Crear Administrador
    admin, created = Usuario.objects.get_or_create(
        correo="admin@servitech.com",
        defaults={
            'nombre_completo': "Administrador Principal",
            'rol': Usuario.Rol.ADMINISTRADOR,
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("[OK] Administrador creado: admin@servitech.com / admin123")
    else:
        print("[*] Administrador existente: admin@servitech.com")

    # 2. Crear Estados de Cita
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

    # 3. Crear Especialidades y Servicios
    esp_gen, _ = Especialidad.objects.get_or_create(nombre='GENERAL', defaults={'descripcion': 'General'})
    esp_cel, _ = Especialidad.objects.get_or_create(nombre='CELULARES', defaults={'descripcion': 'Móviles y Tablets'})
    esp_lap, _ = Especialidad.objects.get_or_create(nombre='LAPTOPS', defaults={'descripcion': 'Computadores Portátiles'})

    servicios = [
        ('Reparación de Pantalla Laptop', 'Sustitución de pantalla', 'LAPTOP', 90, 15, esp_lap),
        ('Cambio de Pantalla OLED', 'Reemplazo de display', 'CELULAR', 60, 10, esp_cel),
        ('Diagnóstico de Rendimiento', 'Evaluación general', 'PC', 60, 10, esp_gen),
        ('Cambio de Batería y Mantenimiento', 'Mantenimiento interno', 'CELULAR', 45, 10, esp_cel)
    ]
    serv_objs = []
    for nombre, desc, disp, dur, buf, esp in servicios:
        obj, _ = Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': desc, 'duracion_minutos': dur, 'buffer_minutos': buf, 'tipo_dispositivo': disp, 'especialidad': esp}
        )
        serv_objs.append(obj)

    # 4. Crear Técnicos
    tecnicos_data = [
        ("Tecnico Celulares", "tec.cel@servitech.com", PerfilTecnico.EspecialidadTecnico.CELULAR),
        ("Tecnico Laptops", "tec.lap@servitech.com", PerfilTecnico.EspecialidadTecnico.LAPTOP),
        ("Tecnico General", "tec.gen@servitech.com", PerfilTecnico.EspecialidadTecnico.GENERAL),
    ]
    tecnicos = []
    for nombre, correo, esp in tecnicos_data:
        t, c = Usuario.objects.get_or_create(
            correo=correo,
            defaults={'nombre_completo': nombre, 'rol': Usuario.Rol.TECNICO}
        )
        if c:
            t.set_password('tecnico123')
            t.save()
            PerfilTecnico.objects.get_or_create(tecnico=t, defaults={'especialidad': esp, 'nivel': PerfilTecnico.Nivel.NIVEL_2})
            print(f"[OK] Tecnico creado: {correo} / tecnico123")
        else:
            PerfilTecnico.objects.get_or_create(tecnico=t, defaults={'especialidad': esp, 'nivel': PerfilTecnico.Nivel.NIVEL_2})
        tecnicos.append(t)

    # 5. Crear Clientes
    clientes_data = [
        ("Ana Torres", "ana.torres@gmail.com", "3001234567"),
        ("Carlos Mendoza", "carlos.mendoza@gmail.com", "3119876543"),
        ("María García", "maria.garcia@gmail.com", "3204567890"),
        ("Roberto López", "roberto.lopez@gmail.com", "3156543210"),
    ]
    clientes = []
    for nombre, correo, tel in clientes_data:
        c, cr = Usuario.objects.get_or_create(
            correo=correo,
            defaults={'nombre_completo': nombre, 'telefono': tel, 'rol': Usuario.Rol.CLIENTE}
        )
        if cr:
            c.set_password('cliente123')
            c.save()
            print(f"[OK] Cliente creado: {correo} / cliente123")
        clientes.append(c)

    # 6. Crear Citas de Prueba
    hoy = date.today()
    citas_test = [
        (clientes[0], serv_objs[0], estados['PENDIENTE'], hoy, time(10, 0), time(11, 30), tecnicos[1]),
        (clientes[1], serv_objs[1], estados['CONFIRMADA'], hoy, time(13, 0), time(14, 0), tecnicos[0]),
        (clientes[2], serv_objs[2], estados['EN_DIAGNOSTICO'], hoy, time(9, 0), time(10, 0), tecnicos[2]),
        (clientes[3], serv_objs[3], estados['FINALIZADA'], hoy - timedelta(days=1), time(15, 0), time(15, 45), tecnicos[0]),
    ]
    for cliente, serv, estado, f, hi, hf, tec in citas_test:
        cita, created_c = Cita.objects.get_or_create(
            cliente=cliente,
            fecha=f,
            hora_inicio=hi,
            defaults={'servicio': serv, 'estado': estado, 'hora_fin': hf, 'tecnico': tec, 'observaciones': 'Prueba autogenerada'}
        )
        if created_c:
            print(f"[OK] Cita creada para {cliente.nombre_completo} ({estado.nombre})")

    print("\n[OK] Datos iniciales listos con exito!")

if __name__ == '__main__':
    run()
