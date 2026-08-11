import codecs
import re

path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

new_finalizar = '''
@login_required
@require_POST
def finalizar_cita(request, cita_id):
    """Permite al técnico marcar una cita como finalizada y descontar repuestos."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado.'}, status=403)

    cita = get_object_or_404(Cita, id=cita_id, tecnico=request.user)
    
    # Process repuestos
    import json
    from turnos.models.inventario import Inventario
    from turnos.models.repuestos import Repuesto
    
    try:
        data = json.loads(request.body)
        repuestos_usados = data.get('repuestos', [])
        
        with transaction.atomic():
            for rep in repuestos_usados:
                rep_id = rep.get('id')
                cantidad = int(rep.get('cantidad', 1))
                
                repuesto = get_object_or_404(Repuesto, id=rep_id)
                
                # Check stock (optional but good)
                if repuesto.stock < cantidad:
                    return JsonResponse({'success': False, 'error': f'Stock insuficiente para {repuesto.nombre}'}, status=400)
                    
                repuesto.stock -= cantidad
                repuesto.save()
                
                Inventario.objects.create(
                    repuesto=repuesto,
                    cantidad=cantidad,
                    tipo='SALIDA',
                    usuario=request.user,
                    cita=cita,
                    motivo=f"Consumo en cita {cita.id} - {cita.servicio.nombre}"
                )
                
            estado_finalizada, _ = EstadoCita.objects.get_or_create(nombre='FINALIZADA')
            cita.estado = estado_finalizada
            cita.save()
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({
        'success': True,
        'message': f'Cita de {cita.cliente.nombre_completo} finalizada con éxito.'
    })
'''

# Use regex to replace the old finalizar_cita view
content = re.sub(
    r'@login_required\s*@require_POST\s*def finalizar_cita\(request, cita_id\):.*?return JsonResponse\(\{.*?\'message\': f\'Cita de \{cita\.cliente\.nombre_completo\} finalizada con \\w+xito\.\'\s*\}\)',
    new_finalizar.strip(),
    content,
    flags=re.DOTALL
)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)

print('Updated finalizar_cita in dashboard_views')
