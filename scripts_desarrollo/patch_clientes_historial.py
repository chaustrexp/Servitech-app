import codecs
import re

# 1. Update urls.py
path_urls = 'c:/Servitech/Servitech-app/turnos/urls.py'
with codecs.open(path_urls, 'r', 'utf-8') as f:
    content_urls = f.read()

new_url = "path('tecnico/clientes/historial-general/', views.tecnico_clientes_historial_general, name='tecnico_clientes_historial_general'),\n    path('tecnico/clientes/', views.tecnico_clientes, name='tecnico_clientes'),"
content_urls = content_urls.replace("path('tecnico/clientes/', views.tecnico_clientes, name='tecnico_clientes'),", new_url)

with codecs.open(path_urls, 'w', 'utf-8') as f:
    f.write(content_urls)


# 2. Update dashboard_views.py
path_views = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path_views, 'r', 'utf-8') as f:
    content_views = f.read()

new_view = '''
@login_required
def tecnico_clientes_historial_general(request):
    """Devuelve el historial general de reparaciones (todas las citas finalizadas) del técnico."""
    if request.user.rol != Usuario.Rol.TECNICO:
        return JsonResponse({'success': False, 'error': 'No autorizado'})
    
    from turnos.models.citas import Cita
    # Solo citas finalizadas del técnico
    citas = Cita.objects.filter(
        tecnico=request.user,
        estado__nombre__icontains='FINALIZ'
    ).select_related('cliente', 'servicio', 'dispositivo').order_by('-fecha', '-hora_inicio')[:50] # Top 50 para no saturar

    data = []
    for c in citas:
        data.append({
            'id': c.id,
            'cliente': c.cliente.nombre_completo,
            'fecha': c.fecha.strftime('%d/%m/%Y'),
            'servicio': c.servicio.nombre,
            'dispositivo': f"{c.dispositivo.marca} {c.dispositivo.modelo}" if c.dispositivo else "Equipo Genérico"
        })
        
    return JsonResponse({'success': True, 'historial': data})
'''
content_views += "\n" + new_view

with codecs.open(path_views, 'w', 'utf-8') as f:
    f.write(content_views)


# 3. Update HTML template
path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_clientes.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    content_html = f.read()

# Insert button in header
header_btn = '''<h2 class="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-2">
            Directorio de Clientes
            <span class="px-2.5 py-0.5 rounded-full bg-[#002b75]/10 text-[#002b75] text-xs font-bold">{{ total_clientes }}</span>
        </h2>
        <p class="text-sm text-slate-500 mt-1 font-medium">Gestiona y revisa el historial clínico de los clientes.</p>
    </div>
    <div class="flex gap-2">
        <button onclick="verHistorialGeneral()" class="bg-blue-50 text-[#002b75] hover:bg-blue-100 border border-blue-200 px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition shadow-sm">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Historial General
        </button>
    </div>'''

content_html = re.sub(
    r'<h2 class="text-2xl font-black text-slate-800 tracking-tight flex items-center gap-2">.*?Gestiona y revisa el historial cl\w+nico de los clientes\.</p>\s*</div>',
    header_btn,
    content_html,
    flags=re.DOTALL
)

# Insert the new modal and JS
new_modal_and_js = '''
<!-- Modal Historial General -->
<div id="modal-historial-general" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" onclick="cerrarHistorialGeneral()"></div>
    <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] z-10 flex flex-col overflow-hidden">
        <div class="bg-emerald-600 px-6 py-4 flex items-center justify-between flex-shrink-0">
            <div>
                <h3 class="text-white font-black text-lg">Historial General de Reparaciones</h3>
                <p class="text-emerald-100 text-sm">Últimos trabajos finalizados</p>
            </div>
            <button onclick="cerrarHistorialGeneral()" class="text-white/60 hover:text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
        </div>
        <div class="p-6 overflow-y-auto flex-1 bg-slate-50" id="mhg-contenido">
            <!-- Contenido dinámico -->
        </div>
    </div>
</div>

<script>
function verHistorialGeneral() {
    document.getElementById('modal-historial-general').classList.remove('hidden');
    document.getElementById('modal-historial-general').classList.add('flex');
    document.body.style.overflow = 'hidden';
    
    document.getElementById('mhg-contenido').innerHTML = `<div class="flex justify-center py-10"><svg class="w-8 h-8 animate-spin text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg></div>`;

    fetch(`/tecnico/clientes/historial-general/`)
        .then(res => res.json())
        .then(data => {
            if(data.success) {
                renderHistorialGeneral(data.historial);
            } else {
                document.getElementById('mhg-contenido').innerHTML = `<p class="text-red-500 text-center py-10">Error al cargar historial: ${data.error}</p>`;
            }
        })
        .catch(err => {
            document.getElementById('mhg-contenido').innerHTML = `<p class="text-red-500 text-center py-10">Error de conexión.</p>`;
        });
}

function cerrarHistorialGeneral() {
    document.getElementById('modal-historial-general').classList.add('hidden');
    document.getElementById('modal-historial-general').classList.remove('flex');
    document.body.style.overflow = '';
}

function renderHistorialGeneral(historial) {
    const cont = document.getElementById('mhg-contenido');
    if(!historial || historial.length === 0) {
        cont.innerHTML = `
        <div class="text-center py-12">
            <div class="w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">🛠️</div>
            <p class="text-slate-500 font-medium">No tienes reparaciones finalizadas aún.</p>
        </div>`;
        return;
    }

    let html = '<div class="space-y-3">';
    historial.forEach(item => {
        html += `
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 flex justify-between items-center hover:border-emerald-300 transition">
            <div>
                <h4 class="font-bold text-slate-800 text-sm">${item.servicio}</h4>
                <p class="text-xs text-slate-500 mt-1"><span class="font-semibold text-slate-600">${item.cliente}</span> • ${item.dispositivo}</p>
            </div>
            <div class="text-right">
                <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">${item.fecha}</span>
            </div>
        </div>
        `;
    });
    html += '</div>';
    cont.innerHTML = html;
}
</script>
'''

content_html = content_html.replace('{% block scripts %}', new_modal_and_js + '\n{% block scripts %}')

with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(content_html)

print('Added Historial General to Directorio de Clientes')
