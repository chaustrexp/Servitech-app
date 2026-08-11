import codecs
import re

path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    content = f.read()

# 1. Update HTML: Find the modal buttons and insert the repuestos-container and the Aceptar button.
# Specifically, we replace the div that contains btn-finalizar-cita and cerrarDetalleCita.
old_buttons = '''<div class="px-5 pb-5 flex gap-2">
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()"
                    class="flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow">
                ✅ Marcar Finalizado
            </button>
            <button onclick="cerrarDetalleCita()"
                    class="flex-1 py-3 rounded-xl border border-slate-200 text-slate-600 font-semibold text-sm hover:bg-slate-50 transition">
                Cerrar
            </button>
        </div>'''

new_buttons = '''<div class="px-5 pb-3 border-t border-slate-100 pt-3" id="repuestos-container">
            <p class="text-[11px] font-bold text-slate-600 uppercase mb-2">Repuestos Utilizados</p>
            <div id="repuestos-input-area" class="space-y-2">
                <div class="flex gap-2">
                    <div class="relative w-1/3">
                        <select id="select-categoria" onchange="filtrarRepuestosEnModal()" class="w-full appearance-none bg-white border border-slate-200 text-slate-600 text-xs font-bold py-2 px-3 rounded-lg shadow-sm focus:outline-none focus:border-[#002b75]">
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
                    <div class="relative w-2/3">
                        <select id="select-repuesto" class="w-full appearance-none bg-white border border-slate-200 text-slate-600 text-xs py-2 px-3 rounded-lg shadow-sm focus:outline-none focus:border-[#002b75]">
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

content = content.replace(old_buttons, new_buttons)


# 2. Update JS variables and parts logic
js_logic = '''
let _activeCitaId = null;
let _repuestosUsados = [];

function filtrarRepuestosEnModal() {
    const categoria = document.getElementById('select-categoria').value;
    const selectRepuesto = document.getElementById('select-repuesto');
    for (let i = 1; i < selectRepuesto.options.length; i++) {
        const option = selectRepuesto.options[i];
        if (categoria === 'ALL' || option.getAttribute('data-categoria') === categoria) {
            option.style.display = '';
        } else {
            option.style.display = 'none';
        }
    }
    selectRepuesto.value = '';
}

function agregarRepuestoACita() {
    const select = document.getElementById('select-repuesto');
    const cantidadInput = document.getElementById('input-cantidad');
    const repuestoId = select.value;
    if (!repuestoId) return;
    const nombre = select.options[select.selectedIndex].getAttribute('data-nombre');
    const cantidad = parseInt(cantidadInput.value);
    if (cantidad < 1) return;
    const index = _repuestosUsados.findIndex(r => r.id === repuestoId);
    if (index >= 0) _repuestosUsados[index].cantidad += cantidad;
    else _repuestosUsados.push({ id: repuestoId, nombre: nombre, cantidad: cantidad });
    renderListaRepuestos();
    select.value = '';
    cantidadInput.value = 1;
}

function renderListaRepuestos() {
    const ul = document.getElementById('lista-repuestos-usados');
    ul.innerHTML = '';
    _repuestosUsados.forEach((r, idx) => {
        ul.innerHTML += `<li class="flex justify-between items-center bg-slate-50 p-2 rounded border border-slate-100">
            <span><b>${r.cantidad}x</b> ${r.nombre}</span>
            <button onclick="removerRepuesto(${idx})" class="text-red-500 hover:text-red-700 font-bold ml-2">✕</button>
        </li>`;
    });
}

function removerRepuesto(idx) {
    _repuestosUsados.splice(idx, 1);
    renderListaRepuestos();
}
'''
content = content.replace("let _activeCitaId = null;", js_logic)

# 3. Update verDetalleCita logic
old_ver_detalle = '''    const btnFinalizar = document.getElementById('btn-finalizar-cita');
    if (btnFinalizar) {
        if (est.includes('FINALIZ')) {
            btnFinalizar.innerHTML = '✅ Finalizado';
            btnFinalizar.disabled = true;
            btnFinalizar.className = 'flex-1 py-3 rounded-xl bg-slate-100 text-slate-400 font-semibold text-sm cursor-not-allowed';
        } else {
            btnFinalizar.innerHTML = '✅ Marcar Finalizado';
            btnFinalizar.disabled = false;
            btnFinalizar.className = 'flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow';
        }
    }'''

new_ver_detalle = '''    const btnAceptar = document.getElementById('btn-aceptar-cita');
    const btnFinalizar = document.getElementById('btn-finalizar-cita');
    const repInputArea = document.getElementById('repuestos-input-area');
    const ul = document.getElementById('lista-repuestos-usados');
    
    // Restablecer
    btnAceptar.classList.add('hidden');
    btnFinalizar.classList.add('hidden');
    repInputArea.classList.add('hidden');
    ul.innerHTML = '';
    btnAceptar.disabled = false;
    btnFinalizar.disabled = false;
    btnAceptar.innerHTML = 'Aceptar Cita';
    btnFinalizar.innerHTML = '✅ Finalizar Cita';
    
    if (est.includes('FINALIZ')) {
        // Mostrar repuestos usados
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
        // En reparación
        btnFinalizar.classList.remove('hidden');
        repInputArea.classList.remove('hidden');
        _repuestosUsados = [];
        const sCat = document.getElementById('select-categoria');
        if(sCat) { sCat.value = 'ALL'; filtrarRepuestosEnModal(); }
        renderListaRepuestos();
    }'''
content = content.replace(old_ver_detalle, new_ver_detalle)

# 4. Update aceptarCitaActiva
new_aceptar = '''
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
content = content.replace("function finalizarCitaActiva() {", new_aceptar + "\nfunction finalizarCitaActiva() {")

# 5. Update finalizarCitaActiva to send repuestos
old_fetch = '''        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }'''
new_fetch = '''        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ repuestos: _repuestosUsados })'''
content = content.replace(old_fetch, new_fetch)

with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(content)

print("Patch applied to clean file successfully.")
