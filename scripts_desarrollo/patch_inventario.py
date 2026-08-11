import codecs
import re

path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_dispositivos.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# 1. Update Mostrando
content = re.sub(
    r'<span class="text-xs text-slate-400 font-medium">Mostrando.*?</span>',
    r'<span data-stock-counter class="text-xs text-slate-400 font-medium">Mostrando {{ repuestos.count }} de {{ repuestos.count }} componentes</span>',
    content
)

# 2. Update Actividad Reciente
new_actividad = '''<h4 class="font-extrabold text-slate-800 text-lg mb-4">Actividad Reciente</h4>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    {% for act in actividad_reciente %}
    <div class="bg-white rounded-2xl border border-slate-100 p-4 shadow-sm flex items-center gap-4 hover:shadow-md transition">
        <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0 text-lg">
            📦
        </div>
        <div>
            <p class="font-bold text-slate-800 text-xs">Salida Servicio</p>
            <p class="text-[11px] text-slate-500 font-medium">{{ act.cantidad }}x {{ act.repuesto.nombre|truncatechars:20 }}</p>
            <p class="text-[10px] text-slate-400 mt-0.5">{{ act.fecha|timesince }}</p>
        </div>
    </div>
    {% empty %}
    <p class="text-xs text-slate-400 italic">No hay salidas recientes.</p>
    {% endfor %}
</div>'''

content = re.sub(
    r'<h4 class="font-extrabold text-slate-800 text-lg mb-4">Actividad Reciente</h4>.*?</div>\s*<!--',
    new_actividad + "\n  <!--",
    content,
    flags=re.DOTALL
)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print('tecnico_dispositivos.html patched')
