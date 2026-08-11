import codecs
path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

old_html = '''        <div class="px-5 pb-5 flex gap-2">
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()"'''

new_html = '''        <div class="px-5 pb-3 border-t border-slate-100 pt-3">
            <p class="text-[11px] font-bold text-slate-600 uppercase mb-2">Repuestos Utilizados</p>
            <div class="space-y-2">
                <select id="select-repuesto" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800">
                    <option value="">-- Ninguno / Seleccionar --</option>
                    {% for r in repuestos %}
                    <option value="{{ r.id }}" data-nombre="{{ r.nombre }}">{{ r.nombre }} (Stock: {{ r.stock }})</option>
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
            <button id="btn-finalizar-cita" onclick="finalizarCitaActiva()"'''

content = content.replace(old_html, new_html)

old_js = '''let _activeCitaId = null;'''
new_js = '''let _activeCitaId = null;
let _repuestosUsados = [];

function agregarRepuestoACita() {
    const select = document.getElementById('select-repuesto');
    const cantidadInput = document.getElementById('input-cantidad');
    
    const repuestoId = select.value;
    if (!repuestoId) return;
    
    const nombre = select.options[select.selectedIndex].getAttribute('data-nombre');
    const cantidad = parseInt(cantidadInput.value);
    
    if (cantidad < 1) return;
    
    // Check if already added
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
content = content.replace(old_js, new_js)

old_js_fetch = '''    fetch(`/tecnico/citas/${_activeCitaId}/finalizar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })'''
new_js_fetch = '''    fetch(`/tecnico/citas/${_activeCitaId}/finalizar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ repuestos: _repuestosUsados })
    })'''
content = content.replace(old_js_fetch, new_js_fetch)

old_js_abrir = '''function abrirDetalleCita(citaId, cliente, servicio, fecha, hora, observaciones) {'''
new_js_abrir = '''function abrirDetalleCita(citaId, cliente, servicio, fecha, hora, observaciones) {
    _repuestosUsados = [];
    renderListaRepuestos();
'''
content = content.replace(old_js_abrir, new_js_abrir)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print('tecnico_agenda.html updated')
