from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Cita, Usuario
from ..forms import EditarPerfilForm

@login_required
def admin_dashboard(request):
    """Dashboard del administrador."""
    return render(request, 'turnos/administracion/admin_dashboard.html')

@login_required
def dashboard_tecnico(request):
    """Dashboard del técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_inicio.html')

@login_required
def tecnico_agenda(request):
    """Agenda del técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_agenda.html')

@login_required
def tecnico_dispositivos(request):
    """Gestión de dispositivos para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_dispositivos.html')

@login_required
def tecnico_clientes(request):
    """Directorio de clientes para el técnico: muestra solo clientes con más de 1 cita."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    from django.db.models import Count
    clientes = (
        Usuario.objects
        .filter(rol=Usuario.Rol.CLIENTE)
        .annotate(total_citas=Count('citas_cliente'))
        .filter(total_citas__gt=1)
        .order_by('-total_citas')
    )

    return render(request, 'turnos/tecnico/tecnico_clientes.html', {'clientes': clientes})


@login_required
def tecnico_soporte(request):
    """Soporte operativo para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_soporte.html')


@login_required
def tecnico_reporte_mensual(request):
    """
    Genera y descarga el reporte mensual del técnico en formato CSV.
    Parámetros GET: mes (1-12), anio (ej. 2026)
    """
    import csv
    from datetime import date
    from django.http import HttpResponse

    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')

    # Leer parámetros, por defecto el mes actual
    hoy = date.today()
    try:
        mes  = int(request.GET.get('mes',  hoy.month))
        anio = int(request.GET.get('anio', hoy.year))
        # Validar rangos
        if not (1 <= mes <= 12):
            mes = hoy.month
        if not (2000 <= anio <= 2100):
            anio = hoy.year
    except (ValueError, TypeError):
        mes, anio = hoy.month, hoy.year

    # Nombres de meses en español
    MESES_ES = {
        1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
        5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto',
        9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'
    }
    nombre_mes = MESES_ES.get(mes, str(mes))

    # Consultar citas del técnico en el mes/año solicitado
    citas = (
        Cita.objects
        .filter(tecnico=request.user, fecha__year=anio, fecha__month=mes)
        .select_related('cliente', 'servicio', 'estado')
        .order_by('fecha', 'hora_inicio')
    )

    # Calcular métricas
    total_citas      = citas.count()
    finalizadas      = citas.filter(estado__nombre='Finalizada').count()
    canceladas       = citas.filter(estado__nombre='Cancelada').count()
    pendientes       = citas.exclude(estado__nombre__in=['Finalizada', 'Cancelada']).count()
    tasa_completado  = f"{round((finalizadas / total_citas * 100), 1)}%" if total_citas > 0 else "0%"

    # Construir respuesta CSV con BOM para Excel
    nombre_archivo = f"reporte_{request.user.nombre_completo.replace(' ', '_')}_{nombre_mes}_{anio}.csv"
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    response.write('\ufeff')  # BOM UTF-8 para compatibilidad con Excel

    writer = csv.writer(response)

    # ── Encabezado del reporte ──────────────────────────────────
    writer.writerow([f'REPORTE MENSUAL DE SERVICIOS — ServiTech'])
    writer.writerow([f'Técnico:',  request.user.nombre_completo])
    writer.writerow([f'Correo:',   request.user.correo])
    writer.writerow([f'Período:',  f'{nombre_mes} {anio}'])
    writer.writerow([f'Generado:', hoy.strftime('%d/%m/%Y')])
    writer.writerow([])

    # ── Resumen ejecutivo ───────────────────────────────────────
    writer.writerow(['RESUMEN DEL MES'])
    writer.writerow(['Total de citas',           total_citas])
    writer.writerow(['Citas finalizadas',         finalizadas])
    writer.writerow(['Citas canceladas',          canceladas])
    writer.writerow(['Citas pendientes/proceso',  pendientes])
    writer.writerow(['Tasa de completado',         tasa_completado])
    writer.writerow([])

    # ── Detalle de citas ────────────────────────────────────────
    writer.writerow(['DETALLE DE CITAS'])
    writer.writerow([
        'N°', 'Fecha', 'Hora Inicio', 'Hora Fin',
        'Cliente', 'Servicio', 'Estado',
        'Retraso (min)', 'Observaciones'
    ])

    for idx, cita in enumerate(citas, start=1):
        writer.writerow([
            idx,
            cita.fecha.strftime('%d/%m/%Y'),
            cita.hora_inicio.strftime('%H:%M'),
            cita.hora_fin.strftime('%H:%M'),
            cita.cliente.nombre_completo,
            cita.servicio.nombre if cita.servicio else '—',
            cita.estado.nombre   if cita.estado   else '—',
            cita.minutos_retraso if cita.minutos_retraso else 0,
            cita.observaciones   if cita.observaciones   else '—',
        ])

    if total_citas == 0:
        writer.writerow(['(Sin citas registradas en este período)', '', '', '', '', '', '', '', ''])

    writer.writerow([])
    writer.writerow(['— Fin del reporte —'])

    return response



@login_required
def cliente_inicio(request):
    """Dashboard principal del cliente (Inicio)"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
        
    citas_usuario = Cita.objects.filter(cliente=request.user).order_by('-fecha', '-hora_inicio')
    
    total_citas_activas = citas_usuario.exclude(estado__nombre__in=['Finalizada', 'Cancelada']).count()
    total_reparaciones = citas_usuario.filter(estado__nombre='Finalizada').count()
    
    citas_recientes = citas_usuario
    
    context = {
        'total_citas_activas': total_citas_activas,
        'total_reparaciones': total_reparaciones,
        'citas_recientes': citas_recientes,
    }
    return render(request, 'turnos/cliente/cliente_inicio.html', context)

@login_required
def cliente_servicios(request):
    """Catálogo de servicios para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente/cliente_servicios.html')

@login_required
def cliente_perfil(request):
    """Perfil del cliente: permite editar datos personales."""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')

    if request.method == 'POST':
        form = EditarPerfilForm(
            request.POST,
            instance=request.user,
            current_user=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tus datos personales fueron actualizados correctamente!')
            return redirect('cliente_perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = EditarPerfilForm(instance=request.user, current_user=request.user)

    return render(request, 'turnos/cliente/cliente_perfil.html', {'form': form})

@login_required
def cliente_soporte(request):
    """Página de soporte para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente/cliente_soporte.html')
