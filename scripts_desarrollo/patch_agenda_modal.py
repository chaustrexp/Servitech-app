import codecs
import re

path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    content_html = f.read()

# 1. Update repuestos-container to have a button filter
new_repuestos = '''<div class="px-5 pb-3 border-t border-slate-100 pt-3" id="repuestos-container">
            <p class="text-[11px] font-bold text-slate-600 uppercase mb-2">Repuestos Utilizados</p>
            <div id="repuestos-input-area" class="space-y-2">
                <div class="flex gap-2">
                    <!-- Boton Filtro -->
                    <div class="relative w-1/3">
                        <select id="select-categoria" onchange="filtrarRepuestosEnModal()" class="w-full appearance-none bg-white border border-slate-200 text-slate-600 text-xs font-bold py-2 px-3 rounded-lg shadow-sm focus:outline-none focus:border-[#002b75] focus:ring-1 focus:ring-[#002b75]">
                            <option value="ALL">Filtro: Todos</option>
                            <option value="PANTALLAS">Pantallas</option>
                            <option value="BATERIAS">Baterías</option>
                            <option value="CONECTORES">Conectores</option>
                            <option value="CAMARAS">Cámaras</option>
                            <option value="MODULOS">Módulos</option>
                            <option value="OTROS">Otros</option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-500">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                        </div>
                    </div>
                    <!-- Select Pieza -->
                    <div class="relative w-2/3">
                        <select id="select-repuesto" class="w-full appearance-none bg-white border border-slate-200 text-slate-600 text-xs py-2 px-3 rounded-lg shadow-sm focus:outline-none focus:border-[#002b75] focus:ring-1 focus:ring-[#002b75]">
                            <option value="">Seleccionar repuesto...</option>
                            {% for r in repuestos %}
                            <option value="{{ r.id }}" data-categoria="{{ r.get_categoria_display|upper }}" data-nombre="{{ r.nombre }}">{{ r.nombre }} (Stock: {{ r.stock }})</option>
                            {% endfor %}
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-500">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                        </div>
                    </div>
                </div>
                <div class="flex gap-2 mt-2">
                    <input type="number" id="input-cantidad" min="1" value="1" class="w-16 bg-white border border-slate-200 rounded-lg px-2 py-2 text-sm text-slate-800 text-center shadow-sm">
                    <button type="button" onclick="agregarRepuestoACita()" class="flex-1 bg-blue-50 hover:bg-blue-100 text-[#002b75] border border-blue-200 text-sm font-bold rounded-lg py-2 transition">Añadir a lista</button>
                </div>
            </div>
            <ul id="lista-repuestos-usados" class="mt-3 space-y-1 text-sm text-slate-600 max-h-24 overflow-y-auto"></ul>
        </div>

        <div class="px-5 pb-5 flex gap-2" id="modal-footer-buttons">
            <button id="btn-aceptar-cita" onclick="aceptarCitaActiva()" class="hidden flex-1 py-3 rounded-xl bg-[#002b75] hover:bg-[#001f54] text-white font-semibold text-sm transition shadow">Aceptar Cita</button>
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()" class="flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow">✅ Finalizar Cita</button>
            <button onclick="cerrarDetalleCita()" class="flex-1 py-3 rounded-xl border border-slate-200 text-slate-600 font-semibold text-sm hover:bg-slate-50 transition">Cerrar</button>
        </div>'''

content_html = re.sub(
    r'<div class="px-5 pb-3 border-t border-slate-100 pt-3" id="repuestos-container">.*?Cerrar\s*</button>\s*</div>',
    new_repuestos,
    content_html,
    flags=re.DOTALL
)

# 2. Update JS in modal
new_js_ver_detalle = '''
    const btnAceptar = document.getElementById('btn-aceptar-cita');
    const btnFinalizar = document.getElementById('btn-finalizar-cita');
    const repInputArea = document.getElementById('repuestos-input-area');
    const ul = document.getElementById('lista-repuestos-usados');
    
    // Configurar visibilidad segun estado
    btnAceptar.classList.add('hidden');
    btnFinalizar.classList.add('hidden');
    repInputArea.classList.add('hidden');
    ul.innerHTML = '';
    
    if (est.includes('FINALIZ')) {
        // Mostrar repuestos ya usados desde la db
        if (cita.repuestos && cita.repuestos.length > 0) {
            cita.repuestos.forEach(r => {
                ul.innerHTML += `<li class="flex justify-between items-center bg-slate-50 p-2 rounded border border-slate-100">
                    <span><b>${r.cantidad}x</b> ${r.nombre}</span>
                </li>`;
            });
        } else {
            ul.innerHTML = `<li class="text-xs text-slate-400 italic">No se registraron repuestos.</li>`;
        }
    } else if (est.includes('NUEVA') || est.includes('PENDIENTE') || est.includes('CONFIRM')) {
        btnAceptar.classList.remove('hidden');
    } else {
        // En progreso / Reparacion
        btnFinalizar.classList.remove('hidden');
        repInputArea.classList.remove('hidden');
        _repuestosUsados = [];
        renderListaRepuestos();
    }
'''

content_html = re.sub(
    r'const btnFinalizar = document.getElementById\(\'btn-finalizar-cita\'\);.*?btnFinalizar\.className = \'flex-1 py-3 rounded-xl bg-slate-100 text-slate-400 font-semibold text-sm cursor-not-allowed\';\s*\} else \{\s*btnFinalizar\.innerHTML = \'✅ Marcar Finalizado\';\s*btnFinalizar\.disabled = false;\s*btnFinalizar\.className = \'flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow\';\s*\}\s*\}',
    new_js_ver_detalle,
    content_html,
    flags=re.DOTALL
)

# Also add aceptarCitaActiva JS function
new_js_aceptar = '''
function aceptarCitaActiva() {
    if (!_activeCitaId) return;
    const btnAceptar = document.getElementById('btn-aceptar-cita');
    btnAceptar.innerHTML = 'Procesando...';
    btnAceptar.disabled = true;
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/tecnico/citas/${_activeCitaId}/aceptar/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }
    }).then(res => res.json()).then(data => {
        if(data.success) { window.location.reload(); }
        else { alert(data.error); btnAceptar.innerHTML = 'Aceptar Cita'; btnAceptar.disabled = false; }
    }).catch(err => {
        alert("Error de conexión");
        btnAceptar.innerHTML = 'Aceptar Cita';
        btnAceptar.disabled = false;
    });
}
'''

content_html = content_html.replace('function finalizarCitaActiva() {', new_js_aceptar + '\nfunction finalizarCitaActiva() {')

with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(content_html)

print('Patched tecnico_agenda.html')
