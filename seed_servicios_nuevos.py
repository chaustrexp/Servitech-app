import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servitech_project.settings')
django.setup()

from turnos.models.servicios import Especialidad, Servicio

def seed():
    print("Iniciando registro del nuevo catálogo de servicios...")
    
    esp_celulares, _ = Especialidad.objects.get_or_create(nombre='CELULARES', defaults={'descripcion': 'Dispositivos móviles'})
    esp_laptops, _ = Especialidad.objects.get_or_create(nombre='LAPTOPS', defaults={'descripcion': 'Computadores portátiles'})
    esp_pc, _ = Especialidad.objects.get_or_create(nombre='PC', defaults={'descripcion': 'Computadores de escritorio'})

    servicios_data = [
        # Celulares
        ('Cambio de Pantalla / Visor', 'Reparación por golpes, táctil inoperativo o manchas en el display.', 'CELULAR', 90, 15, esp_celulares),
        ('Cambio de Batería', 'Sustitución por desgaste de carga o batería hinchada.', 'CELULAR', 45, 10, esp_celulares),
        ('Reparación de Pin de Carga', 'Solución a sulfatación o falso contacto al conectar el cargador.', 'CELULAR', 60, 10, esp_celulares),
        ('Flasheo y Software', 'Corrección de equipos bloqueados en el logo o fallos de arranque.', 'CELULAR', 60, 15, esp_celulares),
        
        # Laptops
        ('Mantenimiento y Pasta Térmica', 'Limpieza profunda de ventiladores para evitar sobrecalentamiento.', 'LAPTOP', 90, 15, esp_laptops),
        ('Reemplazo de Pantalla', 'Cambio de panel LED/LCD dañado o parpadeante.', 'LAPTOP', 60, 10, esp_laptops),
        ('Reparación de Bisagras y Chasis', 'Reconstrucción mecánica de soportes y tapas quebradas.', 'LAPTOP', 120, 20, esp_laptops),
        ('Cambio de Teclado / Batería', 'Sustitución de componentes desgastados o con fallas por humedad.', 'LAPTOP', 60, 10, esp_laptops),
        
        # PC de Escritorio
        ('Mantenimiento Preventivo', 'Eliminación de polvo interno, lubricación y cambio de pasta térmica.', 'PC', 90, 15, esp_pc),
        ('Formateo y Sistema Operativo', 'Instalación limpia de sistema operativo, controladores y programas básicos.', 'PC', 120, 15, esp_pc),
        ('Upgrade de SSD / Memoria RAM', 'Clonación de disco duro y optimización de velocidad.', 'PC', 60, 10, esp_pc),
        ('Diagnóstico de Encendido', 'Detección de fallas en fuente de poder o tarjeta madre.', 'PC', 60, 10, esp_pc),
    ]

    # Inactivar servicios anteriores para que el catálogo quede limpio
    Servicio.objects.update(activo=False)

    for nombre, desc, disp, dur, buf, esp_obj in servicios_data:
        obj, created = Servicio.objects.update_or_create(
            nombre=nombre,
            defaults={
                'descripcion': desc,
                'tipo_dispositivo': disp,
                'duracion_minutos': dur,
                'buffer_minutos': buf,
                'especialidad': esp_obj,
                'activo': True
            }
        )
        if created:
            print(f"  [NUEVO] Servicio registrado: {nombre}")
        else:
            print(f"  [ACTUALIZADO] Servicio: {nombre}")

    print("¡Catálogo de servicios actualizado con éxito!")

if __name__ == '__main__':
    seed()
