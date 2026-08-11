import codecs
import re

path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/administracion/admin_tecnicos.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    content = f.read()

# normalize newlines to make replacement easy
content = content.replace('\r\n', '\n')

# 1. Password input
yellow_box = '''                    <div class="bg-[#fefce8] border border-[#fef08a] rounded-lg px-4 py-3 flex items-start gap-3">
                        <svg class="w-4 h-4 text-[#ca8a04] mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                        <p class="text-[12px] text-[#a16207] font-medium">Se genera contraseña temporal automáticamente.</p>
                    </div>'''

password_input = '''                    <div>
                        <label class="block text-[12px] font-bold text-slate-700 mb-1.5">Contraseña *</label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                            </div>
                            <input type="text" name="password" id="inp-password-nuevo" placeholder="Escriba la contraseña a asignar"
                                   class="w-full pl-9 pr-3 py-2 border border-slate-200 rounded-lg text-[13px] focus:outline-none focus:border-[#0e3687] focus:ring-1 focus:ring-[#0e3687]" required>
                        </div>
                    </div>'''

if yellow_box in content:
    content = content.replace(yellow_box, password_input)
else:
    print('WARNING: Yellow box not found')

# 2. Status colors
old_badge = '''                    <span class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider
                        {% if estado == 'en_proceso' %}bg-[#4ade80] text-emerald-900
                        {% elif estado == 'disponible' %}bg-blue-100 text-[#0e3687]
                        {% elif estado == 'pausado' %}bg-rose-100 text-rose-800
                        {% else %}bg-slate-100 text-slate-500{% endif %}">
                        {% if estado == 'en_proceso' %}En proceso
                        {% elif estado == 'disponible' %}Disponible
                        {% elif estado == 'pausado' %}Con novedad
                        {% else %}Inactivo{% endif %}
                    </span>'''

new_badge = '''                    <span class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider
                        {% if estado == 'en_proceso' %}bg-[#22c55e] text-white
                        {% elif estado == 'disponible' %}bg-blue-100 text-[#0e3687]
                        {% elif estado == 'pausado' %}bg-[#eab308] text-white
                        {% else %}bg-[#ef4444] text-white{% endif %}">
                        {% if estado == 'en_proceso' %}En proceso
                        {% elif estado == 'disponible' %}Disponible
                        {% elif estado == 'pausado' %}En pausa
                        {% else %}Inactivo{% endif %}
                    </span>'''

if old_badge in content:
    content = content.replace(old_badge, new_badge)
else:
    print('WARNING: Old badge not found')
    
# also the little dot in the icon header
old_dot = '''                        <svg class="w-4 h-4 flex-shrink-0 mt-0.5
                            {% if estado == 'en_proceso' %}text-emerald-700{% elif estado == 'pausado' %}text-rose-600{% else %}text-slate-500{% endif %}"'''

new_dot = '''                        <svg class="w-4 h-4 flex-shrink-0 mt-0.5
                            {% if estado == 'en_proceso' %}text-[#22c55e]{% elif estado == 'pausado' %}text-[#eab308]{% else %}text-[#ef4444]{% endif %}"'''
                            
if old_dot in content:
    content = content.replace(old_dot, new_dot)

old_card = '''                <div class="rounded-xl p-4 mb-4
                    {% if estado == 'en_proceso' %}bg-[#dcfce7]
                    {% elif estado == 'pausado' %}bg-rose-50
                    {% else %}bg-slate-50{% endif %}">'''

new_card = '''                <div class="rounded-xl p-4 mb-4
                    {% if estado == 'en_proceso' %}bg-[#dcfce7]
                    {% elif estado == 'pausado' %}bg-[#fefce8]
                    {% else %}bg-slate-50{% endif %}">'''

if old_card in content:
    content = content.replace(old_card, new_card)
    
with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(content)

print('Patched admin_tecnicos.html successfully.')
