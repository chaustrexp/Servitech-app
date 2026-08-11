import codecs
import re

path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

new_aceptar = '''@login_required
@require_POST
def aceptar_cita(request, cita_id):
    """Permite al técnico aceptar una cita y pasarla a EN REPARACION."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    cita = get_object_or_404(Cita, id=cita_id)
    
    # Check if someone else owns it
    if cita.tecnico is not None and cita.tecnico != request.user:
        return JsonResponse({'success': False, 'error': 'Esta cita ya tiene un técnico asignado.'}, status=400)

    # Asignar técnico (si no lo tenía)
    cita.tecnico = request.user
    
    # Cambiar estado a EN REPARACION
    from turnos.models.citas import EstadoCita
    estado_rep, _ = EstadoCita.objects.get_or_create(nombre='EN REPARACION')
    cita.estado = estado_rep
    
    cita.save()

    return JsonResponse({
        'success': True,
        'message': f'Cita de {cita.cliente.nombre_completo} iniciada con éxito.'
    })'''

content = re.sub(
    r'@login_required\s*@require_POST\s*def aceptar_cita\(request, cita_id\):.*?return JsonResponse\(\{.*?\}\)',
    new_aceptar,
    content,
    flags=re.DOTALL
)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)

print('Updated aceptar_cita')
