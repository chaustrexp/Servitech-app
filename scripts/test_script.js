
function abrirModal(id) {
    document.getElementById(id).classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function cerrarModal(id) {
    document.getElementById(id).classList.add('hidden');
    document.body.style.overflow = '';
}
['modal-crear-tecnico','modal-editar-perfil','modal-asignar'].forEach(id => {
    document.getElementById(id).addEventListener('click', function(e) {
        if (e.target === this) cerrarModal(id);
    });
});
function switchTab(actId, inactId) {
    document.getElementById(actId).classList.add('active');
    document.getElementById(inactId).classList.remove('active');
    const map = {'tab-nuevo':'panel-nuevo','tab-vincular':'panel-vincular'};
    document.getElementById(map[actId]).classList.remove('hidden');
    document.getElementById(map[inactId]).classList.add('hidden');
}
function abrirModalEditarPerfil(id, nombre, genero, especialidad, observaciones) {
    document.getElementById('edit-tecnico-id').value = id;
    document.getElementById('edit-tecnico-nombre').textContent = nombre;
    
    const generoElement = document.getElementById('edit-genero');
    if (generoElement) {
        if (genero === 'M' || genero === 'hombre') {
            generoElement.value = 'hombre';
        } else if (genero === 'F' || genero === 'mujer') {
            generoElement.value = 'mujer';
        } else {
            generoElement.value = 'hombre'; // Default
        }
    }
    
    document.querySelectorAll('.edit-esp-check').forEach(c => { 
        c.checked = (c.value === especialidad); 
    });
    const obsElement = document.getElementById('edit-observaciones');
    if(obsElement) {
        obsElement.value = (observaciones === 'None') ? '' : observaciones;
    }
    abrirModal('modal-editar-perfil');
}
function abrirModalAsignar(id, nombre) {
    document.getElementById('modal-tecnico-id').value = id;
    document.getElementById('modal-tecnico-nombre').textContent = nombre;
    abrirModal('modal-asignar');
}
function abrirModalAsignarCita(citaId) {
    const r = document.getElementById('asignar-cita-' + citaId);
    if (r) r.checked = true;
    abrirModal('modal-asignar');
}
document.getElementById('sel-usuario-existente').addEventListener('change', function() {
    const n = this.options[this.selectedIndex].dataset.nombre || '';
    document.getElementById('inp-nombre-nuevo').value = n;
});
