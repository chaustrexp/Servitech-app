import codecs
path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

old_code = '''def finalizar_cita(request, cita_id):
    """Permite al tǸcnico marcar una cita como finalizada."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    cita = get_object_or_404(Cita, id=cita_id, tecnico=request.user)
    
    # Obtener o crear el estado FINALIZADA
    estado_finalizada, _ = EstadoCita.objects.get_or_create(nombre='FINALIZADA')
    
    cita.estado = estado_finalizada
    cita.save()

    return JsonResponse({
        'success': True,
        'message': f'Cita de {cita.cliente.nombre_completo} finalizada con Ǹxito.'
    })'''

new_code = '''import json
from django.db import transaction

@login_required
@require_POST
def finalizar_cita(request, cita_id):
    """Permite al técnico marcar una cita como finalizada y descontar repuestos."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    cita = get_object_or_404(Cita, id=cita_id, tecnico=request.user)
    
    try:
        data = json.loads(request.body)
        repuestos_usados = data.get('repuestos', [])
    except Exception:
        repuestos_usados = []

    from ..models import Repuesto, Inventario
    
    with transaction.atomic():
        # Procesar repuestos
        for item in repuestos_usados:
            try:
                rep_id = item.get('id')
                cantidad = int(item.get('cantidad', 1))
                
                repuesto = Repuesto.objects.select_for_update().get(id=rep_id)
                if repuesto.stock >= cantidad:
                    repuesto.stock -= cantidad
                    repuesto.save()
                    
                    Inventario.objects.create(
                        repuesto=repuesto,
                        cantidad=cantidad,
                        tipo='SALIDA',
                        usuario=request.user,
                        cita=cita,
                        motivo=f'Uso en Cita #{cita.id}'
                    )
            except Exception as e:
                pass # Ignorar errores individuales para no bloquear la finalizacion

        # Obtener o crear el estado FINALIZADA
        estado_finalizada, _ = EstadoCita.objects.get_or_create(nombre='FINALIZADA')
        
        cita.estado = estado_finalizada
        cita.save()

    return JsonResponse({
        'success': True,
        'message': f'Cita de {cita.cliente.nombre_completo} finalizada con éxito.'
    })'''

content = content.replace(old_code, new_code)
with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print('finalizar_cita patched')
