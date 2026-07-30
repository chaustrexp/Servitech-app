from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from datetime import datetime, timedelta

from .models import Cita, Usuario, Especialidad, Servicio, EstadoCita
from .forms import RegistroUsuarioForm, CustomLoginForm, EditarPerfilForm


# ────────────────────────────────────────────────────────────────
#  AUTENTICACIÓN
# ────────────────────────────────────────────────────────────────

class RegistroView(SuccessMessageMixin, CreateView):
    """
    Registro público de nuevos usuarios (rol CLIENTE por defecto).
    Redirige al login tras el registro exitoso.
    """
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'turnos/registro.html'
    success_url = reverse_lazy('login')
    success_message = "¡Tu cuenta ha sido creada exitosamente! Por favor, inicia sesión."

    def dispatch(self, request, *args, **kwargs):
        # Si ya está autenticado, va directo al inicio
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Login usando correo electrónico como identificador.
    Si el usuario ya está autenticado, lo lleva directo al home.
    """
    form_class = CustomLoginForm
    template_name = 'turnos/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, "Correo electrónico o contraseña incorrectos.")
        return super().form_invalid(form)


# ────────────────────────────────────────────────────────────────
#  HOME — Redirección según Rol
# ────────────────────────────────────────────────────────────────

def home(request):
    """
    Punto de entrada. Si no está autenticado, va al login.
    Si está autenticado, redirige según su rol.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    rol = request.user.rol
    if rol == Usuario.Rol.ADMINISTRADOR:
        return redirect('admin_dashboard')
    elif rol == Usuario.Rol.TECNICO:
        return redirect('dashboard_tecnico')
    else:
        # CLIENTE y RECEPCIONISTA van al dashboard principal
        return redirect('cliente_inicio')


# ────────────────────────────────────────────────────────────────
#  AGENDAMIENTO / DISPOSITIVO
# ────────────────────────────────────────────────────────────────

@login_required
def seleccionar_dispositivo(request):
    """Paso 1 del wizard de agendamiento: seleccionar tipo de dispositivo."""
    if request.method == 'POST':
        dispositivo = request.POST.get('dispositivo')
        if dispositivo:
            request.session['wizard_dispositivo'] = dispositivo
            return redirect('seleccionar_servicio')
    return render(request, 'turnos/seleccionar_dispositivo.html')

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
            
    return render(request, 'turnos/seleccionar_servicio.html', {'dispositivo': dispositivo})

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
            
    return render(request, 'turnos/seleccionar_fecha_hora.html', {
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
        # El valor del dispositivo ya viene en UPPERCASE (CELULAR, LAPTOP, PC)
        tipo_dispositivo = dispositivo  # ya es CELULAR / LAPTOP / PC

        # Obtener o crear Especialidad y Servicio
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

        # Parsear fecha y calcular hora fin
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora, '%H:%M').time()
        hora_fin = (datetime.combine(fecha_obj, hora_inicio)
                    + timedelta(minutes=servicio_obj.duracion_minutos)).time()

        # Estado Confirmada
        estado, _ = EstadoCita.objects.get_or_create(nombre='Confirmada')

        # Crear la cita en BD
        cita = Cita.objects.create(
            cliente=request.user,
            servicio=servicio_obj,
            estado=estado,
            fecha=fecha_obj,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            observaciones=f'Dispositivo: {dispositivo}',
        )

        # Limpiar sesión del wizard
        for key in ['wizard_dispositivo', 'wizard_servicio', 'wizard_fecha', 'wizard_hora']:
            request.session.pop(key, None)

        return redirect('cita_confirmada', cita_id=cita.pk)

    return render(request, 'turnos/resumen_cita.html', {
        'dispositivo': dispositivo,
        'servicio': servicio_nombre,
        'fecha': fecha,
        'hora': hora,
    })


@login_required
def cita_confirmada(request, cita_id):
    """Vista de éxito post-confirmación de cita."""
    cita = get_object_or_404(Cita, pk=cita_id, cliente=request.user)

    # Extraer dispositivo (almacenado como CELULAR/LAPTOP/PC en observaciones)
    dispositivo_map = {'CELULAR': 'Celular', 'LAPTOP': 'Laptop', 'PC': 'PC'}
    raw = ''
    if cita.observaciones and cita.observaciones.startswith('Dispositivo: '):
        raw = cita.observaciones.replace('Dispositivo: ', '', 1)
    dispositivo_display = dispositivo_map.get(raw, raw) or cita.servicio.tipo_dispositivo.title()

    # Construir enlace Google Calendar
    fecha_str = cita.fecha.strftime('%Y%m%d')
    hi_str = cita.hora_inicio.strftime('%H%M%S')
    hf_str = cita.hora_fin.strftime('%H%M%S')
    gcal_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text=Cita+ServiTech+-+{cita.servicio.nombre.replace(' ', '+')}"
        f"&dates={fecha_str}T{hi_str}/{fecha_str}T{hf_str}"
        f"&details=Cita+%23ST-{cita.pk}+en+ServiTech"
    )

    return render(request, 'turnos/cita_confirmada.html', {
        'cita': cita,
        'dispositivo': dispositivo_display,
        'gcal_url': gcal_url,
    })


@login_required
def detalle_cita(request, cita_id):
    """Ticket completo de la cita para el cliente."""
    cita = get_object_or_404(Cita, pk=cita_id, cliente=request.user)

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

    # Extraer dispositivo (CELULAR/LAPTOP/PC -> label legible)
    dispositivo_map = {'CELULAR': 'Celular', 'LAPTOP': 'Laptop', 'PC': 'PC'}
    raw = ''
    if cita.observaciones and cita.observaciones.startswith('Dispositivo: '):
        raw = cita.observaciones.replace('Dispositivo: ', '', 1)
    dispositivo_display = dispositivo_map.get(raw, raw) or cita.servicio.tipo_dispositivo.title()

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

    return render(request, 'turnos/detalle_cita.html', {
        'cita': cita,
        'dispositivo': dispositivo_display,
        'estado_nombre': estado_nombre,
        'estados_progreso': estados_progreso,
        'estado_actual_idx': estado_actual_idx,
    })


# ────────────────────────────────────────────────────────────────
#  DASHBOARDS (Placeholder hasta implementación completa)
# ────────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    """Dashboard del administrador."""
    return render(request, 'turnos/admin_dashboard.html')


@login_required
def dashboard_tecnico(request):
    """Dashboard del técnico."""
    return render(request, 'turnos/dashboard_tecnico.html')


# ────────────────────────────────────────────────────────────────
#  TURNOS DIGITALES
# ────────────────────────────────────────────────────────────────

def ver_turno(request, turno_id):
    """Muestra la vista pública del turno digital."""
    turno = get_object_or_404(Cita, pk=turno_id)
    return render(request, 'turnos/turno_digital.html', {'turno': turno})


# ────────────────────────────────────────────────────────────────
#  DASHBOARD CLIENTE
# ────────────────────────────────────────────────────────────────

@login_required
def cliente_inicio(request):
    """Dashboard principal del cliente (Inicio)"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
        
    citas_usuario = Cita.objects.filter(cliente=request.user).order_by('-fecha', '-hora_inicio')
    
    # Calcular KPIs
    total_citas_activas = citas_usuario.exclude(estado__nombre__in=['Finalizada', 'Cancelada']).count()
    total_reparaciones = citas_usuario.filter(estado__nombre='Finalizada').count()
    
    # Citas recientes (para la lista completa con toggle JS)
    citas_recientes = citas_usuario
    
    context = {
        'total_citas_activas': total_citas_activas,
        'total_reparaciones': total_reparaciones,
        'citas_recientes': citas_recientes,
    }
    return render(request, 'turnos/cliente_inicio.html', context)

@login_required
def cliente_servicios(request):
    """Catálogo de servicios para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente_servicios.html')

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

    return render(request, 'turnos/cliente_perfil.html', {'form': form})

@login_required
def cliente_soporte(request):
    """Página de soporte para el cliente"""
    if request.user.rol != Usuario.Rol.CLIENTE:
        return redirect('home')
    return render(request, 'turnos/cliente_soporte.html')


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
