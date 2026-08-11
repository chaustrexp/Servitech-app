from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta

from ..models import Cita, Especialidad, Servicio, EstadoCita, Usuario
from ..services.asignacion import asignar_tecnico, NoTechnicianAvailable


@login_required
def seleccionar_dispositivo(request):
    """Paso 1 del wizard de agendamiento: seleccionar tipo de dispositivo."""
    if request.method == 'POST':
        dispositivo = request.POST.get('dispositivo')
        if dispositivo:
            request.session['wizard_dispositivo'] = dispositivo
            return redirect('seleccionar_servicio')
    return render(request, 'turnos/cliente/agendamiento/seleccionar_dispositivo.html')

@login_required
def seleccionar_servicio(request):
    """Paso 2 del wizard: seleccionar servicio."""
    dispositivo = request.session.get('wizard_dispositivo')
    if not dispositivo:
        return redirect('seleccionar_dispositivo')
        
    if request.method == 'POST':
        servicio = request.POST.get('servicio')
        if servicio:
            request.session['wizard_servicio'] = servicio
            return redirect('seleccionar_fecha_hora')
            
    servicios_disponibles = Servicio.objects.filter(tipo_dispositivo__iexact=dispositivo, activo=True)
            
    return render(request, 'turnos/cliente/agendamiento/seleccionar_servicio.html', {
        'dispositivo': dispositivo,
        'servicios_disponibles': servicios_disponibles
    })

@login_required
def seleccionar_fecha_hora(request):
    """Paso 3 del wizard: seleccionar fecha y hora."""
    dispositivo = request.session.get('wizard_dispositivo')
    servicio = request.session.get('wizard_servicio')
    if not dispositivo or not servicio:
        return redirect('seleccionar_dispositivo')
        
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        if fecha and hora:
            request.session['wizard_fecha'] = fecha
            request.session['wizard_hora'] = hora
            return redirect('resumen_cita')
            
    return render(request, 'turnos/cliente/agendamiento/seleccionar_fecha_hora.html', {
        'dispositivo': dispositivo,
        'servicio': servicio
    })

@login_required
def resumen_cita(request):
    """Paso 4 del wizard: resumen y confirmación."""
    dispositivo = request.session.get('wizard_dispositivo')
    servicio_nombre = request.session.get('wizard_servicio')
    fecha = request.session.get('wizard_fecha')
    hora = request.session.get('wizard_hora')

    if not all([dispositivo, servicio_nombre, fecha, hora]):
        return redirect('seleccionar_dispositivo')

    if request.method == 'POST':
        tipo_dispositivo = dispositivo

        especialidad, _ = Especialidad.objects.get_or_create(
            nombre='General',
            defaults={'descripcion': 'Servicio técnico general'}
        )
        servicio_obj, _ = Servicio.objects.get_or_create(
            nombre=servicio_nombre,
            defaults={
                'tipo_dispositivo': tipo_dispositivo,
                'duracion_minutos': 60,
                'especialidad': especialidad,
            }
        )

        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora, '%H:%M').time()
        hora_fin = (datetime.combine(fecha_obj, hora_inicio)
                    + timedelta(minutes=servicio_obj.duracion_minutos)).time()

        estado, _ = EstadoCita.objects.get_or_create(nombre='Confirmada')

        notas_usuario = (request.POST.get('observaciones') or request.POST.get('notas') or '').strip()

        try:
            tecnico_asignado = asignar_tecnico(fecha_obj, hora_inicio, tipo_dispositivo)
        except NoTechnicianAvailable as e:
            messages.error(request, str(e))
            return redirect('seleccionar_fecha_hora')

        cita = Cita.objects.create(
            cliente=request.user,
            tecnico=tecnico_asignado,
            servicio=servicio_obj,
            estado=estado,
            fecha=fecha_obj,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            observaciones=notas_usuario if notas_usuario else None,
        )

        for key in ['wizard_dispositivo', 'wizard_servicio', 'wizard_fecha', 'wizard_hora']:
            request.session.pop(key, None)

        return redirect('cita_confirmada', cita_id=cita.pk)

    return render(request, 'turnos/cliente/agendamiento/resumen_cita.html', {
        'dispositivo': dispositivo,
        'servicio': servicio_nombre,
        'fecha': fecha,
        'hora': hora,
    })

@login_required
def cita_confirmada(request, cita_id):
    """Vista de éxito post-confirmación de cita."""
    cita = get_object_or_404(Cita, pk=cita_id)
    if request.user != cita.cliente and request.user != cita.tecnico and request.user.rol != Usuario.Rol.ADMINISTRADOR:
        from django.http import Http404
        raise Http404('No tienes permiso para ver esta cita.')

    dispositivo_map = {'CELULAR': 'Celular', 'LAPTOP': 'Laptop', 'PC': 'PC'}
    tipo_disp = cita.servicio.tipo_dispositivo.upper() if cita.servicio and cita.servicio.tipo_dispositivo else ''
    dispositivo_display = dispositivo_map.get(tipo_disp, cita.servicio.tipo_dispositivo.title() if cita.servicio and cita.servicio.tipo_dispositivo else 'Equipo')

    fecha_str = cita.fecha.strftime('%Y%m%d')
    hi_str = cita.hora_inicio.strftime('%H%M%S')
    hf_str = cita.hora_fin.strftime('%H%M%S')
    gcal_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text=Cita+ServiTech+-+{cita.servicio.nombre.replace(' ', '+')}"
        f"&dates={fecha_str}T{hi_str}/{fecha_str}T{hf_str}"
        f"&details=Cita+%23ST-{cita.pk}+en+ServiTech"
    )

    return render(request, 'turnos/cliente/agendamiento/cita_confirmada.html', {
        'cita': cita,
        'dispositivo': dispositivo_display,
        'gcal_url': gcal_url,
    })

@login_required
def detalle_cita(request, cita_id):
    """Ticket completo de la cita para el cliente."""
    cita = get_object_or_404(Cita, pk=cita_id)
    if request.user != cita.cliente and request.user != cita.tecnico and request.user.rol != Usuario.Rol.ADMINISTRADOR:
        from django.http import Http404
        raise Http404('No tienes permiso para ver esta cita.')

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'retraso':
            minutos = int(request.POST.get('minutos', 10))
            if cita.minutos_retraso == 0:
                cita.minutos_retraso = minutos
                cita.save()
                messages.success(request, f'Retraso de {minutos} min notificado correctamente.')
            else:
                messages.warning(request, 'Ya notificaste un retraso para esta cita.')

        elif accion == 'cancelar':
            estado_cancelada, _ = EstadoCita.objects.get_or_create(nombre='Cancelada')
            cita.estado = estado_cancelada
            cita.save()
            messages.success(request, 'Cita cancelada exitosamente.')
            return redirect('home')

        return redirect('detalle_cita', cita_id=cita.pk)

    dispositivo_map = {'CELULAR': 'Celular', 'LAPTOP': 'Laptop', 'PC': 'PC'}
    tipo_disp = cita.servicio.tipo_dispositivo.upper() if cita.servicio and cita.servicio.tipo_dispositivo else ''
    dispositivo_display = dispositivo_map.get(tipo_disp, cita.servicio.tipo_dispositivo.title() if cita.servicio and cita.servicio.tipo_dispositivo else 'Equipo')

    estado_nombre = cita.estado.nombre if cita.estado else 'Confirmada'
    estados_progreso = [
        {'nombre': 'Creada',      'icono': 'check'},
        {'nombre': 'Confirmada',  'icono': 'calendar'},
        {'nombre': 'Diagnóstico', 'icono': 'wrench'},
        {'nombre': 'Finalizada',  'icono': 'flag'},
    ]
    estado_actual_idx = next(
        (i for i, e in enumerate(estados_progreso) if e['nombre'] == estado_nombre), 1
    )

    return render(request, 'turnos/contingencias/detalle_cita.html', {
        'cita': cita,
        'dispositivo': dispositivo_display,
        'estado_nombre': estado_nombre,
        'estados_progreso': estados_progreso,
        'estado_actual_idx': estado_actual_idx,
    })

def ver_turno(request, turno_id):
    """Muestra la vista pública del turno digital."""
    turno = get_object_or_404(Cita, pk=turno_id)
    return render(request, 'turnos/contingencias/turno_digital.html', {'turno': turno})

@login_required
def notificar_retraso(request, turno_id):
    """
    RF-04: El cliente notifica que llegará ~10 minutos tarde.
    Solo permite notificar una vez por turno.
    """
    turno = get_object_or_404(Cita, pk=turno_id, cliente=request.user)

    if request.method == "POST":
        if turno.minutos_retraso == 0:
            turno.minutos_retraso = 10
            turno.save()
            messages.success(request, "Notificación de retraso enviada correctamente.")
        else:
            messages.warning(request, "Ya notificaste un retraso para este turno.")

    return redirect('ver_turno', turno_id=turno.pk)
