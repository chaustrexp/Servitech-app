from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from ..models import Usuario
from ..forms import RegistroUsuarioForm, CustomLoginForm

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
