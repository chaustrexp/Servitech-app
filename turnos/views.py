from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Cita, Usuario
from .forms import RegistroUsuarioForm, CustomLoginForm


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
        # CLIENTE y RECEPCIONISTA van al agendamiento
        return redirect('seleccionar_dispositivo')


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
    servicio = request.session.get('wizard_servicio')
    fecha = request.session.get('wizard_fecha')
    hora = request.session.get('wizard_hora')
    
    if not all([dispositivo, servicio, fecha, hora]):
        return redirect('seleccionar_dispositivo')
        
    if request.method == 'POST':
        # Aquí se crearía la Cita en base de datos.
        # Cita.objects.create(...)
        # Limpiar sesión:
        for key in ['wizard_dispositivo', 'wizard_servicio', 'wizard_fecha', 'wizard_hora']:
            if key in request.session:
                del request.session[key]
        messages.success(request, "¡Cita confirmada exitosamente!")
        return redirect('home')
        
    return render(request, 'turnos/resumen_cita.html', {
        'dispositivo': dispositivo,
        'servicio': servicio,
        'fecha': fecha,
        'hora': hora
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
