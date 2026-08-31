import random
from datetime import date, time, datetime, timedelta
from django.db.models import Count, Q
from turnos.models import Usuario
from turnos.models.tecnicos import PerfilTecnico

class NoTechnicianAvailable(Exception):
    """Excepción lanzada cuando no hay ningún técnico disponible para la asignación."""
    pass

# Configuración: Permite limitar a los técnicos a un máximo estricto de 1 cita activa por bloque de horario
LIMITAR_UNA_CITA_POR_BLOQUE = True

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

    # Técnicos especialistas (coincidencia exacta), con fallback al técnico general
    if especialidad_req:
        tecnicos_especialistas = tecnicos_base.filter(
            perfil_tecnico__especialidad=especialidad_req
        )
        tecnicos_generales = tecnicos_base.filter(
            perfil_tecnico__especialidad=PerfilTecnico.EspecialidadTecnico.GENERAL
        )
    else:
        tecnicos_especialistas = tecnicos_base
        tecnicos_generales = tecnicos_base.none()

    if not tecnicos_especialistas.exists() and not tecnicos_generales.exists():
        raise NoTechnicianAvailable("No hay técnicos con la especialidad requerida activos.")

    # 2. Filtrar por HorarioTecnico (Obligatorio)
    dia_semana = fecha.weekday()  # 0 = Lunes, 6 = Domingo

    hora_inicio_dt = datetime.combine(fecha, hora_inicio)
    hora_fin = (hora_inicio_dt + timedelta(hours=1)).time()

    def filtrar_por_horario(qs):
        return qs.filter(
            horarios__dia_semana=dia_semana,
            horarios__hora_inicio__lte=hora_inicio,
            horarios__hora_fin__gte=hora_fin
        ).distinct()

    especialistas_disponibles = filtrar_por_horario(tecnicos_especialistas)
    generales_disponibles = filtrar_por_horario(tecnicos_generales)

    # Prioridad: especialistas primero, generales como fallback
    if especialistas_disponibles.exists():
        tecnicos_horario = especialistas_disponibles
    elif generales_disponibles.exists():
        tecnicos_horario = generales_disponibles
    else:
        raise NoTechnicianAvailable("Ningún técnico capacitado tiene horario de trabajo en este bloque.")

    # 3. Contar citas en ese bloque (excluir CANCELADA y FINALIZADA)
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

    # 4. Elegir el de menor carga; en empate, aleatorio
    min_citas = tecnicos_con_citas.first().citas_en_bloque

    # Si la regla de 1 cita por bloque está activa y todos los técnicos ya tienen al menos 1 cita:
    if LIMITAR_UNA_CITA_POR_BLOQUE and min_citas >= 1:
        raise NoTechnicianAvailable("Todos los técnicos capacitados están ocupados en este bloque de horario.")

    candidatos_finales = [t for t in tecnicos_con_citas if t.citas_en_bloque == min_citas]

    return random.choice(candidatos_finales)
