import codecs
import re

path = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

new_cita_data = '''        estado:       "{{ cita.estado.nombre|escapejs }}",
        observaciones:"{{ cita.observaciones|default:''|escapejs }}",
        repuestos: [
            {% for inv in cita.repuestos_usados.all %}
            { id: "{{ inv.id }}", nombre: "{{ inv.repuesto.nombre|escapejs }}", cantidad: {{ inv.cantidad }} }{% if not forloop.last %},{% endif %}
            {% endfor %}
        ]
    }'''

content = re.sub(r'estado:\s*"\{\{ cita\.estado\.nombre\|escapejs \}\}",\s*observaciones:"\{\{ cita\.observaciones\|default:\'\'\|escapejs \}\}"[ \t\n]*\}', new_cita_data, content, flags=re.DOTALL)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)
print('Added CITAS_DATA repuestos back')
