import os

# 1. Update dashboard_views.py
views_path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace tecnico_toggle_pausa
old_toggle = '''def tecnico_toggle_pausa(request):
    """
    Alterna el estado de pausa manual del técnico.
    """
    if request.method == 'POST' and request.user.rol == Usuario.Rol.TECNICO:
        try:
            perfil = request.user.perfil_tecnico
            
            # Si quiere pausar, verificar que no tenga citas activas
            if not perfil.en_pausa_manual:
                from django.utils import timezone
                from datetime import date
                hoy = timezone.now().date()
                citas_activas = request.user.citas_asignadas.filter(
                    fecha=hoy
                ).exclude(estado__nombre__in=['Cancelada', 'Completada', 'No asistió'])
                
                if citas_activas.exists():
                    messages.error(request, "No puedes pausar tu turno mientras tengas citas activas o pendientes.")
                    return redirect('dashboard_tecnico')
                    
            perfil.en_pausa_manual = not perfil.en_pausa_manual
            perfil.save(update_fields=['en_pausa_manual'])
            
            estado_msg = "EN PAUSA" if perfil.en_pausa_manual else "DISPONIBLE"
            messages.success(request, f"Turno actualizado. Ahora estás {estado_msg}.")
        except Exception as e:
            messages.error(request, f"Error al cambiar estado: {e}")
            
    return redirect('dashboard_tecnico')'''

new_toggle = '''from django.http import JsonResponse

def tecnico_toggle_pausa(request):
    """
    Alterna el estado de pausa manual del técnico. Soporta AJAX.
    """
    if request.method == 'POST' and request.user.rol == Usuario.Rol.TECNICO:
        try:
            perfil = request.user.perfil_tecnico
            
            if not perfil.en_pausa_manual:
                from django.utils import timezone
                hoy = timezone.now().date()
                citas_activas = request.user.citas_asignadas.filter(
                    fecha=hoy
                ).exclude(estado__nombre__in=['Cancelada', 'Completada', 'No asistió'])
                
                if citas_activas.exists():
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({'success': False, 'error': "No puedes pausar tu turno mientras tengas citas activas o pendientes."})
                    messages.error(request, "No puedes pausar tu turno mientras tengas citas activas o pendientes.")
                    return redirect('dashboard_tecnico')
                    
            perfil.en_pausa_manual = not perfil.en_pausa_manual
            perfil.save(update_fields=['en_pausa_manual'])
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': True, 'pausado': perfil.en_pausa_manual})
                
            estado_msg = "EN PAUSA" if perfil.en_pausa_manual else "DISPONIBLE"
            messages.success(request, f"Turno actualizado. Ahora estás {estado_msg}.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Error al cambiar estado: {e}")
            
    return redirect('dashboard_tecnico')

def api_estado_tecnicos(request):
    """
    Devuelve el estado de todos los técnicos para actualizar el panel de admin en tiempo real.
    """
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        
    tecnicos = Usuario.objects.filter(rol=Usuario.Rol.TECNICO, is_active=True)
    data = []
    
    from django.utils import timezone
    hoy = timezone.now().date()
    ahora = timezone.now().time()
    
    for t in tecnicos:
        perfil = t.perfil_tecnico if hasattr(t, 'perfil_tecnico') else None
        estado = 'disponible'
        
        if perfil and perfil.en_pausa_manual:
            estado = 'pausado'
        else:
            cita_activa = t.citas_asignadas.filter(
                fecha=hoy, 
                hora_inicio__lte=ahora, 
                hora_fin__gte=ahora
            ).exclude(estado__nombre__in=['Cancelada', 'Completada', 'No asistió']).first()
            if cita_activa:
                estado = 'en_proceso'
                
        data.append({
            'id': t.pk,
            'estado': estado
        })
        
    return JsonResponse({'success': True, 'tecnicos': data})'''

content = content.replace(old_toggle, new_toggle)
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update urls.py
urls_path = 'c:/Servitech/Servitech-app/turnos/urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    content = f.read()

url_pattern = "path('tecnico/toggle-pausa/', views.tecnico_toggle_pausa, name='tecnico_toggle_pausa'),"
new_url = "path('tecnico/toggle-pausa/', views.tecnico_toggle_pausa, name='tecnico_toggle_pausa'),\n    path('api/estado-tecnicos/', views.api_estado_tecnicos, name='api_estado_tecnicos'),"
if "path('api/estado-tecnicos/'," not in content:
    content = content.replace(url_pattern, new_url)
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Update tecnico_base.html
base_path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to change togglePausarTurno to actually send fetch
old_js = '''            if (turnoPausado) {
                texto.textContent = 'Reanudar Turno';'''
new_js = '''
            // Envío Ajax
            fetch('/tecnico/toggle-pausa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    mostrarToast(data.error, 'error');
                    turnoPausado = !turnoPausado; // revertir
                    return;
                }
            });

            if (turnoPausado) {
                texto.textContent = 'Reanudar Turno';'''
if "// Envío Ajax" not in content:
    content = content.replace(old_js, new_js)
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 4. Update admin_tecnicos.html
admin_path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/administracion/admin_tecnicos.html'
with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_div_start = '''<div class="flex flex-col items-end gap-1.5 flex-shrink-0">
                    <span class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider
                        {% if estado == 'en_proceso' %}bg-[#22c55e] text-white
                        {% elif estado == 'disponible' %}bg-blue-100 text-[#0e3687]
                        {% elif estado == 'pausado' %}bg-[#eab308] text-white
                        {% else %}bg-[#ef4444] text-white{% endif %}">
                        {% if estado == 'en_proceso' %}En proceso
                        {% elif estado == 'disponible' %}Disponible
                        {% elif estado == 'pausado' %}En pausa
                        {% else %}Inactivo{% endif %}
                    </span>'''
new_div_start = '''<div class="flex flex-col items-end gap-1.5 flex-shrink-0">
                    <span id="badge-tecnico-{{ t.pk }}" class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider
                        {% if estado == 'en_proceso' %}bg-[#22c55e] text-white
                        {% elif estado == 'disponible' %}bg-blue-100 text-[#0e3687]
                        {% elif estado == 'pausado' %}bg-[#eab308] text-white
                        {% else %}bg-[#ef4444] text-white{% endif %}">
                        {% if estado == 'en_proceso' %}En proceso
                        {% elif estado == 'disponible' %}Disponible
                        {% elif estado == 'pausado' %}En pausa
                        {% else %}Inactivo{% endif %}
                    </span>'''
content = content.replace(old_div_start, new_div_start)

# Add polling script at the end
script_block = '''
{% block scripts %}
<script>
    // Polling estado de tecnicos
    setInterval(() => {
        fetch("{% url 'api_estado_tecnicos' %}")
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                data.tecnicos.forEach(t => {
                    const badge = document.getElementById('badge-tecnico-' + t.id);
                    if(badge) {
                        if(t.estado === 'en_proceso') {
                            badge.className = 'text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-[#22c55e] text-white';
                            badge.textContent = 'En proceso';
                        } else if(t.estado === 'disponible') {
                            badge.className = 'text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-blue-100 text-[#0e3687]';
                            badge.textContent = 'Disponible';
                        } else if(t.estado === 'pausado') {
                            badge.className = 'text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-[#eab308] text-white';
                            badge.textContent = 'En pausa';
                        } else {
                            badge.className = 'text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-[#ef4444] text-white';
                            badge.textContent = 'Inactivo';
                        }
                    }
                });
            }
        });
    }, 5000);
</script>
{% endblock %}
'''
if "api_estado_tecnicos" not in content:
    if "{% block scripts %}" in content:
        content = content.replace("{% block scripts %}", script_block.replace("{% block scripts %}", "{% block scripts %}"))
    else:
        content += script_block
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
