import codecs

path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'a', 'utf-8') as f:
    f.write('''
@login_required
def tecnico_cliente_historial(request, cliente_id):
    """Devuelve el historial clínico completo de los dispositivos de un cliente en formato JSON."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado'})

    try:
        cliente = Usuario.objects.get(id=cliente_id, rol=Usuario.Rol.CLIENTE)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})

    from turnos.models.dispositivos import Dispositivo
    from turnos.models.citas import Cita

    # Obtener dispositivos del cliente
    dispositivos = Dispositivo.objects.filter(cliente=cliente).order_by('-fecha_registro')
    
    # También buscamos citas que no tengan dispositivo asignado y las agrupamos bajo "Dispositivo Genérico"
    citas_sin_dispositivo = Cita.objects.filter(cliente=cliente, dispositivo__isnull=True).order_by('-fecha', '-hora_inicio')

    data_dispositivos = []

    for disp in dispositivos:
        citas_disp = Cita.objects.filter(dispositivo=disp).order_by('-fecha', '-hora_inicio')
        if citas_disp.exists():
            citas_data = [{
                'id': c.id,
                'servicio': c.servicio.nombre,
                'fecha': c.fecha.strftime('%d/%m/%Y'),
                'estado': c.estado.nombre.upper() if c.estado else 'PENDIENTE',
                'observaciones': c.observaciones or ''
            } for c in citas_disp]
            
            data_dispositivos.append({
                'id': disp.id,
                'marca': disp.marca,
                'modelo': disp.modelo,
                'imei_serial': disp.imei_serial,
                'citas': citas_data
            })

    if citas_sin_dispositivo.exists():
        citas_data = [{
            'id': c.id,
            'servicio': c.servicio.nombre,
            'fecha': c.fecha.strftime('%d/%m/%Y'),
            'estado': c.estado.nombre.upper() if c.estado else 'PENDIENTE',
            'observaciones': c.observaciones or ''
        } for c in citas_sin_dispositivo]
        
        data_dispositivos.append({
            'id': 0,
            'marca': 'Equipo',
            'modelo': 'Generico',
            'imei_serial': 'No registrado',
            'citas': citas_data
        })

    return JsonResponse({'success': True, 'dispositivos': data_dispositivos})
''')
print("View appended")
