import os
import re

# 1. Update views
views_path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

old_view = '''@login_required
def tecnico_soporte(request):
    """Soporte operativo para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
    return render(request, 'turnos/tecnico/tecnico_soporte.html')'''

new_view = '''from turnos.models.soporte import TicketSoporte, EstadoSistema
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def tecnico_soporte(request):
    """Soporte operativo para el técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return redirect('home')
        
    tickets = TicketSoporte.objects.filter(tecnico=request.user).order_by('-fecha_creacion')
    sistemas = EstadoSistema.objects.all().order_by('nombre')
    
    context = {
        'tickets': tickets,
        'sistemas': sistemas
    }
    return render(request, 'turnos/tecnico/tecnico_soporte.html', context)

@login_required
@require_POST
def tecnico_crear_ticket(request):
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        
    try:
        data = json.loads(request.body)
        titulo = data.get('titulo')
        area = data.get('area')
        urgencia = data.get('urgencia')
        descripcion = data.get('descripcion')
        
        ticket = TicketSoporte.objects.create(
            titulo=titulo,
            area=area,
            urgencia=urgencia,
            descripcion=descripcion,
            tecnico=request.user
        )
        return JsonResponse({'success': True, 'message': 'Ticket creado con éxito'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
'''

if old_view in views_content:
    views_content = views_content.replace(old_view, new_view)
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(views_content)
    print("Updated views!")

# 2. Update urls.py
urls_path = 'c:/Servitech/Servitech-app/turnos/urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

old_url = "path('tecnico/soporte/', views.tecnico_soporte, name='tecnico_soporte'),"
new_url = "path('tecnico/soporte/', views.tecnico_soporte, name='tecnico_soporte'),\n    path('tecnico/soporte/crear/', views.tecnico_crear_ticket, name='tecnico_crear_ticket'),"

if old_url in urls_content:
    urls_content = urls_content.replace(old_url, new_url)
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("Updated urls!")

# 3. Also update __init__.py for views
init_path = 'c:/Servitech/Servitech-app/turnos/views/__init__.py'
with open(init_path, 'r', encoding='utf-8') as f:
    init_content = f.read()

old_init = "tecnico_soporte,"
new_init = "tecnico_soporte,\n    tecnico_crear_ticket,"
if old_init in init_content:
    init_content = init_content.replace(old_init, new_init)
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(init_content)
    print("Updated view init!")

