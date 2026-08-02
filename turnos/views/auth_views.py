from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login

from ..models import Usuario
from ..forms import RegistroUsuarioForm, CustomLoginForm

class RegistroView(SuccessMessageMixin, CreateView):
    """
    Registro público de nuevos usuarios (rol CLIENTE por defecto).
    Redirige al login tras el registro exitoso.
    """
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'turnos/auth/registro.html'
    success_url = reverse_lazy('login')
    success_message = "¡Tu cuenta ha sido creada exitosamente! Por favor, inicia sesión."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """
    Login con soporte de sesiones separadas por rol.
    Permite tener activos simultáneamente un Cliente y un Técnico en pestañas distintas.
    La sesión expira automáticamente al cerrar la pestaña/navegador (SESSION_EXPIRE_AT_BROWSER_CLOSE=True).
    Si el usuario marca "Recordarme", la sesión persiste.
    """
    form_class = CustomLoginForm
    template_name = 'turnos/auth/login.html'
    redirect_authenticated_user = False  # Desactivamos la redirección automática para manejarla nosotros

    def dispatch(self, request, *args, **kwargs):
        role_context = request.POST.get('role_context') or request.GET.get('role_context', 'cliente')

        # Si el usuario ya está autenticado en esta cookie de sesión concreta,
        # redirigir directamente a su dashboard
        if request.user.is_authenticated:
            rol = request.user.rol
            # Si el rol activo en esta sesión coincide con el solicitado, redirigir
            if role_context == 'tecnico' and rol == Usuario.Rol.TECNICO:
                return redirect('dashboard_tecnico')
            elif role_context == 'cliente' and rol in [Usuario.Rol.CLIENTE, Usuario.Rol.RECEPCIONISTA]:
                return redirect('cliente_inicio')
            elif role_context == 'admin' and rol == Usuario.Rol.ADMINISTRADOR:
                return redirect('admin_dashboard')
            # Si hay una sesión activa con distinto rol, permitir continuar para iniciar otra sesión

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        """
        Manejar 'Recordarme' y redirigir DIRECTAMENTE al dashboard del rol.
        Saltamos la ruta neutra '/' para que el middleware encuentre la cookie correcta
        en la redirección (la misma cookie guardada durante el POST del login).
        """
        user = form.get_user()
        remember_me = self.request.POST.get('remember')

        # Configurar duración de la sesión según "Recordarme"
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            self.request.session.set_expiry(0)

        auth_login(self.request, user)

        # Redirigir directamente al portal correcto según el rol del usuario
        rol = user.rol
        if rol == Usuario.Rol.ADMINISTRADOR:
            return redirect('admin_dashboard')
        elif rol == Usuario.Rol.TECNICO:
            return redirect('dashboard_tecnico')
        else:
            return redirect('cliente_inicio')

    def form_invalid(self, form):
        messages.error(self.request, "Correo electrónico o contraseña incorrectos.")
        return super().form_invalid(form)

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
        return redirect('cliente_inicio')

