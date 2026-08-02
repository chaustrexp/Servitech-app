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
    form_class = CustomLoginForm
    template_name = 'turnos/auth/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        # Siempre redirigir a home, ignorar ?next=
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        remember_me = self.request.POST.get('remember')
        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            self.request.session.set_expiry(0)

        auth_login(self.request, user)

        print(f"[LOGIN] Usuario: {user.correo} | Rol: {user.rol} | Activo: {user.is_active}")

        rol = user.rol
        if rol == Usuario.Rol.ADMINISTRADOR:
            print("[LOGIN] Redirigiendo a admin_dashboard")
            return redirect('admin_dashboard')
        elif rol == Usuario.Rol.TECNICO:
            print("[LOGIN] Redirigiendo a dashboard_tecnico")
            return redirect('dashboard_tecnico')
        else:
            print("[LOGIN] Redirigiendo a cliente_inicio")
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
    elif rol == Usuario.Rol.CLIENTE:
        return redirect('cliente_inicio')
    else:
        # Rol no reconocido — evita el bucle, va al login con mensaje
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')

