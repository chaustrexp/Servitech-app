from datetime import datetime, timedelta
from django.utils import timezone
from turnos.models import Cita, EstadoCita

def cancelar_citas_vencidas():
    """
    Verifica y cancela automáticamente aquellas citas que hayan superado
    la ventana de tolerancia de 15 minutos (más los minutos de retraso notificados)
    sin haber sido aceptadas/iniciadas por el técnico.
    """
    ahora = timezone.localtime(timezone.now()) if timezone.is_aware(timezone.now()) else datetime.now()
    fecha_actual = ahora.date()
    
    # Citas candidatas: fecha de hoy o pasada, en estados previos a la atención
    estados_evaluar = ['PENDIENTE', 'CONFIRMADA', 'RETRASADA']
    
    citas_candidatas = Cita.objects.filter(
        fecha__lte=fecha_actual,
        estado__nombre__in=estados_evaluar
    ).select_related('estado', 'cliente', 'servicio')
    
    estado_cancelada, _ = EstadoCita.objects.get_or_create(nombre='CANCELADA')
    canceladas = []
    
    for cita in citas_candidatas:
        dt_inicio = datetime.combine(cita.fecha, cita.hora_inicio)
        if timezone.is_aware(ahora):
            from django.utils.timezone import get_current_timezone
            dt_inicio = timezone.make_aware(dt_inicio, get_current_timezone())
            
        tolerancia_minutos = 15 + (cita.minutos_retraso or 0)
        dt_limite = dt_inicio + timedelta(minutes=tolerancia_minutos)
        
        # Si la hora actual es posterior al límite de tolerancia
        if ahora >= dt_limite:
            cita.estado = estado_cancelada
            obs_nota = f"[Cancelada automáticamente por inasistencia (tolerancia de {tolerancia_minutos} min superada)]"
            if cita.observaciones:
                if "[Cancelada automáticamente por inasistencia" not in cita.observaciones:
                    cita.observaciones = f"{cita.observaciones} | {obs_nota}"
            else:
                cita.observaciones = obs_nota
            cita.save()

            # Crear notificación en la plataforma para el cliente
            try:
                from turnos.models.notificaciones import Notificacion
                if not Notificacion.objects.filter(cita=cita, tipo='CANCELACION_INASISTENCIA').exists():
                    nombre_serv = cita.servicio.nombre if cita.servicio else "Servicio técnico"
                    hora_str = cita.hora_inicio.strftime('%I:%M %p') if cita.hora_inicio else ""
                    fecha_str = cita.fecha.strftime('%d/%m/%Y') if cita.fecha else ""
                    Notificacion.objects.create(
                        usuario=cita.cliente,
                        cita=cita,
                        tipo='CANCELACION_INASISTENCIA',
                        mensaje=f"Tu cita para {nombre_serv} programada el {fecha_str} a las {hora_str} fue cancelada automáticamente por inasistencia tras 15 minutos de tolerancia."
                    )
            except Exception:
                pass

            canceladas.append(cita)
            
    return canceladas
