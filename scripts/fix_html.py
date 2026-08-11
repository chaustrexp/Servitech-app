import os

filepath = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_soporte.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace tickets list
tickets_start = content.find('<div id="lista-tickets" class="divide-y divide-slate-100">')
tickets_end = content.find('<!-- Footer -->')

if tickets_start != -1 and tickets_end != -1:
    new_tickets = '''<div id="lista-tickets" class="divide-y divide-slate-100">
            {% for ticket in tickets %}
            <div class="ticket-item p-4 hover:bg-slate-50 transition-all cursor-pointer flex items-center gap-4 group"
                 data-estado="{{ ticket.estado }}"
                 onclick="verTicket('{{ ticket.titulo|escapejs }}', '{{ ticket.fecha_creacion|date:"d M Y H:i" }}', '{{ ticket.urgencia }}', '{{ ticket.area }}', '{{ ticket.descripcion|escapejs }}', '{{ ticket.estado }}')">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0
                    {% if ticket.estado == 'abierto' %}bg-red-50 text-red-500
                    {% elif ticket.estado == 'revision' %}bg-blue-50 text-blue-500
                    {% elif ticket.estado == 'resuelto' %}bg-emerald-50 text-emerald-500
                    {% else %}bg-slate-100 text-slate-500{% endif %}">
                    {% if ticket.estado == 'abierto' %}
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                    {% elif ticket.estado == 'revision' %}
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582 4 8 4"/></svg>
                    {% elif ticket.estado == 'resuelto' %}
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    {% else %}
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                    {% endif %}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="font-bold text-slate-800 text-sm truncate">{{ ticket.titulo }}</p>
                    <p class="text-xs text-slate-400 mt-0.5">Reportado {{ ticket.fecha_creacion|timesince }} atrás · Urgencia: {{ ticket.get_urgencia_display }}</p>
                </div>
                <span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase tracking-wider flex-shrink-0
                    {% if ticket.estado == 'abierto' %}bg-red-100 text-red-700
                    {% elif ticket.estado == 'revision' %}bg-amber-100 text-amber-700
                    {% elif ticket.estado == 'resuelto' %}bg-emerald-100 text-emerald-700
                    {% else %}bg-slate-100 text-slate-700{% endif %}">
                    {{ ticket.get_estado_display }}
                </span>
                <svg class="w-4 h-4 text-slate-300 group-hover:text-[#002b75] flex-shrink-0 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </div>
            {% empty %}
            <div class="p-8 text-center">
                <p class="text-sm font-bold text-slate-500">No tienes tickets de soporte registrados.</p>
            </div>
            {% endfor %}
        </div>

        '''
    content = content[:tickets_start] + new_tickets + content[tickets_end:]


# 2. Replace Estado de Sistemas
sys_start_str = '<div class="space-y-3">'
sys_start = content.find(sys_start_str, content.find('Estado de Sistemas'))
sys_end_str = '</div>\n        </div>\n\n    </div>\n</div>'
sys_end = content.find(sys_end_str, sys_start)

if sys_start != -1 and sys_end != -1:
    new_sys = '''<div class="space-y-3">
                {% for sis in sistemas %}
                <button onclick="abrirEstadoSistema('{{ sis.nombre|escapejs }}', '{{ sis.estado }}', '{{ sis.detalle|escapejs }}')"
                        class="w-full flex items-center justify-between hover:bg-slate-50 p-1.5 rounded-xl transition-all">
                    <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full flex-shrink-0 {% if sis.estado == 'operativo' %}bg-emerald-500{% elif sis.estado == 'mantenimiento' %}bg-amber-400 animate-pulse{% else %}bg-red-500 animate-pulse{% endif %}"></span>
                        <span class="text-sm font-semibold text-slate-700">{{ sis.nombre }}</span>
                    </div>
                    <span class="text-xs font-extrabold uppercase tracking-wider {% if sis.estado == 'operativo' %}text-emerald-600{% elif sis.estado == 'mantenimiento' %}text-amber-600{% else %}text-red-600{% endif %}">
                        {{ sis.get_estado_display }}
                    </span>
                </button>
                {% empty %}
                <p class="text-xs text-slate-400 text-center py-4">No hay sistemas registrados</p>
                {% endfor %}
            </div>'''
    content = content[:sys_start] + new_sys + content[sys_end:]


# 3. Modify enviarTicket js function
old_enviar = '''function enviarTicket(e) {
        e.preventDefault();
        const titulo = document.getElementById('nt-titulo').value;
        cerrarNuevoTicket();
        mostrarToast(`✅ Solicitud "${titulo}" enviada al equipo de soporte`, 'success');
        e.target.reset();
    }'''

new_enviar = '''function enviarTicket(e) {
        e.preventDefault();
        const titulo = document.getElementById('nt-titulo').value;
        const area = document.getElementById('nt-area').value;
        const urgencia = document.getElementById('nt-urgencia').value;
        const desc = document.getElementById('nt-desc').value;
        
        fetch("{% url 'tecnico_crear_ticket' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ titulo: titulo, area: area, urgencia: urgencia, descripcion: desc })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                cerrarNuevoTicket();
                mostrarToast(`✅ Solicitud "${titulo}" enviada con éxito`, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                mostrarToast('Error: ' + data.error, 'error');
            }
        });
    }'''

content = content.replace(old_enviar, new_enviar)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Template updated successfully")
