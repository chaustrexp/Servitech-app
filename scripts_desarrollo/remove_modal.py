import codecs
path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_dispositivos.html'
with codecs.open(path, 'r', 'utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '<button onclick="abrirModalNuevoRepuesto()"' in line:
        skip = True
    if skip and '</button>' in line and 'M12 4v16m8-8H4' in lines[i-2]:
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

lines = new_lines
new_lines = []
skip = False
for i, line in enumerate(lines):
    if '<!-- MODAL: AGREGAR NUEVO REPUESTO -->' in line:
        skip = True
    if skip and '</div>' in line and '</div>' in lines[i-1] and '</form>' in lines[i-2]:
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

lines = new_lines
new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'function abrirModalNuevoRepuesto()' in line:
        skip = True
    if skip and '}' in line and 'cerrarModalNuevoRepuesto' in lines[i-3]:
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

with codecs.open(path, 'w', 'utf-8') as f:
    f.writelines(new_lines)
print('Template updated')
