import codecs

path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

old_html = '''        </div>
        <div class="px-5 pb-5 flex gap-2">
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()"
                    class="flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow">
                ✅ Marcar Finalizado
            </button>'''

new_html = '''        </div>
        <div class="px-5 pb-3 border-t border-slate-100 pt-3" id="repuestos-container">
            <p class="text-[11px] font-bold text-slate-600 uppercase mb-2">Repuestos Utilizados</p>
            <div class="space-y-2">
                <select id="select-categoria" onchange="filtrarRepuestosEnModal()" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 mb-2">
                    <option value="ALL">-- Todas las categorías --</option>
                    <option value="PANTALLAS">Pantallas / LCD</option>
                    <option value="BATERIAS">Baterías</option>
                    <option value="CONECTORES">Conectores</option>
                    <option value="CAMARAS">Cámaras</option>
                    <option value="MODULOS">Módulos</option>
                    <option value="OTROS">Otros</option>
                </select>
                <select id="select-repuesto" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800">
                    <option value="">-- Ninguno / Seleccionar --</option>
                    {% for r in repuestos %}
                    <option value="{{ r.id }}" data-categoria="{{ r.categoria }}" data-nombre="{{ r.nombre }}">{{ r.nombre }} (Stock: {{ r.stock }})</option>
                    {% endfor %}
                </select>
                <div class="flex gap-2">
                    <input type="number" id="input-cantidad" min="1" value="1" class="w-20 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 text-center">
                    <button type="button" onclick="agregarRepuestoACita()" class="flex-1 bg-[#002b75] hover:bg-[#001f54] text-white text-sm font-bold rounded-lg py-2 transition">Añadir a lista</button>
                </div>
            </div>
            <ul id="lista-repuestos-usados" class="mt-3 space-y-1 text-sm text-slate-600 max-h-24 overflow-y-auto"></ul>
        </div>
        <div class="px-5 pb-5 flex gap-2">
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()"
                    class="flex-1 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition shadow">
                ✅ Marcar Finalizado
            </button>'''

if old_html in content:
    content = content.replace(old_html, new_html)
else:
    print("HTML not found!")

old_js = '''let _activeCitaId = null;'''

new_js = '''let _activeCitaId = null;
let _repuestosUsados = [];

function filtrarRepuestosEnModal() {
    const categoria = document.getElementById('select-categoria').value;
    const selectRepuesto = document.getElementById('select-repuesto');
    
    // Iterar sobre las opciones saltando la primera ("Ninguno")
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
    if (index >= 0) {
        _repuestosUsados[index].cantidad += cantidad;
    } else {
        _repuestosUsados.push({ id: repuestoId, nombre: nombre, cantidad: cantidad });
    }
    
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

if old_js in content:
    content = content.replace(old_js, new_js)
else:
    print("JS not found!")

old_fetch = '''    fetch(`/tecnico/citas/${_activeCitaId}/finalizar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })'''

new_fetch = '''    fetch(`/tecnico/citas/${_activeCitaId}/finalizar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ repuestos: _repuestosUsados })
    })'''

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch)
else:
    print("Fetch not found!")

old_open = '''function abrirDetalleCita(citaId, cliente, servicio, fecha, hora, observaciones) {'''
new_open = '''function abrirDetalleCita(citaId, cliente, servicio, fecha, hora, observaciones) {
    _repuestosUsados = [];
    renderListaRepuestos();
    document.getElementById('select-categoria').value = 'ALL';
    filtrarRepuestosEnModal();
'''

# Wait, `abrirDetalleCita` is not defined in `tecnico_agenda.html` ? No, wait!
# It is actually `verDetalleCita(citaId)`. Let's check `verDetalleCita` inside the file.
old_open_correct = '''function verDetalleCita(citaId) {'''
new_open_correct = '''function verDetalleCita(citaId) {
    _repuestosUsados = [];
    renderListaRepuestos();
    document.getElementById('select-categoria').value = 'ALL';
    filtrarRepuestosEnModal();
'''
if old_open_correct in content:
    content = content.replace(old_open_correct, new_open_correct)
else:
    print("verDetalleCita not found!")

old_finalized_state = '''    if (btnFinalizar) {
        if (est.includes('FINALIZ')) {
            btnFinalizar.innerHTML = '✅ Finalizado';
            btnFinalizar.disabled = true;
            btnFinalizar.className = 'flex-1 py-3 rounded-xl bg-slate-100 text-slate-400 font-semibold text-sm cursor-not-allowed';
        } else {'''

new_finalized_state = '''    const repCont = document.getElementById('repuestos-container');
    if (btnFinalizar) {
        if (est.includes('FINALIZ')) {
            btnFinalizar.innerHTML = '✅ Finalizado';
            btnFinalizar.disabled = true;
            btnFinalizar.className = 'flex-1 py-3 rounded-xl bg-slate-100 text-slate-400 font-semibold text-sm cursor-not-allowed';
            if(repCont) repCont.classList.add('hidden');
        } else {
            if(repCont) repCont.classList.remove('hidden');
'''
if old_finalized_state in content:
    content = content.replace(old_finalized_state, new_finalized_state)
else:
    print("finalized state not found!")


with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print("tecnico_agenda.html updated")
