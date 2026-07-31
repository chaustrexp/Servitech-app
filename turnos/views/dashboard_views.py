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
