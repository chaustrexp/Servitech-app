import random
from datetime import date, time, datetime, timedelta
from django.db.models import Count, Q
from turnos.models import Usuario
from turnos.models.tecnicos import PerfilTecnico

class NoTechnicianAvailable(Exception):
    """Excepción lanzada cuando no hay ningún técnico disponible para la asignación."""
    pass

def asignar_tecnico(fecha: date, hora_inicio: time, tipo_equipo: str) -> Usuario:
    """
    Asigna un técnico disponible basado en especialidad, horario, y menor carga de trabajo.
    """
    # 1. Mapear especialidad
    # tipo_equipo expected values are 'CELULAR', 'LAPTOP', 'PC'
    map_especialidad = {
        'CELULAR': PerfilTecnico.EspecialidadTecnico.CELULAR,
        'LAPTOP': PerfilTecnico.EspecialidadTecnico.LAPTOP,
        'PC': PerfilTecnico.EspecialidadTecnico.PC,
    }
    especialidad_req = map_especialidad.get(tipo_equipo.upper())

    # Técnicos activos con perfil que no estén en pausa
    tecnicos_base = Usuario.objects.filter(
        rol=Usuario.Rol.TECNICO,
        activo=True,
        perfil_tecnico__isnull=False,
        perfil_tecnico__en_pausa_manual=False
    )

    if especialidad_req:
        tecnicos_esp = tecnicos_base.filter(
            Q(perfil_tecnico__especialidad=especialidad_req) |
            Q(perfil_tecnico__especialidad=PerfilTecnico.EspecialidadTecnico.GENERAL)
        )
    else:
        tecnicos_esp = tecnicos_base

    if not tecnicos_esp.exists():
        raise NoTechnicianAvailable("No hay técnicos con la especialidad requerida activos.")

    # 2. Filtrar por HorarioTecnico (Obligatorio)
    dia_semana = fecha.weekday() # 0 = Lunes, 6 = Domingo
    
    # Calcular la hora de fin (1 hora después) para ver si cabe en su horario
    hora_inicio_dt = datetime.combine(fecha, hora_inicio)
    hora_fin_dt = hora_inicio_dt + timedelta(hours=1)
    hora_fin = hora_fin_dt.time()

    tecnicos_horario = tecnicos_esp.filter(
        horarios__dia_semana=dia_semana,
        horarios__hora_inicio__lte=hora_inicio,
        horarios__hora_fin__gte=hora_fin
    ).distinct()

    if not tecnicos_horario.exists():
        raise NoTechnicianAvailable("Ningún técnico capacitado tiene horario de trabajo en este bloque.")

    # 3. Contar Citas en esa fecha y bloque (Excluir CANCELADA y FINALIZADA)
    estados_ocupados = ['PENDIENTE', 'CONFIRMADA', 'RETRASADA', 'EN_DIAGNOSTICO', 'EN_REPARACION']
    
    tecnicos_con_citas = tecnicos_horario.annotate(
        citas_en_bloque=Count(
            'citas_tecnico',
            filter=Q(
                citas_tecnico__fecha=fecha,
                citas_tecnico__hora_inicio=hora_inicio,
                citas_tecnico__estado__nombre__in=estados_ocupados
            )
        )
    ).order_by('citas_en_bloque')

    # 4. Desempate: seleccionar al que menos tiene. Si hay empate, random.
    min_citas = tecnicos_con_citas.first().citas_en_bloque
    candidatos_finales = [t for t in tecnicos_con_citas if t.citas_en_bloque == min_citas]

    return random.choice(candidatos_finales)
