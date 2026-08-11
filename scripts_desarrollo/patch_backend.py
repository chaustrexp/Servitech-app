import codecs

path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# I need to add repuestos_usados to the cita dictionary sent to template
import re
new_data = '''
    # Pre-cargar repuestos usados para que puedan ser enviados al frontend
    from turnos.models.inventario import Inventario
    
    # We will build CITAS_DATA more manually, but since it's rendered in template, 
    # we just attach them to the objects
    for cita in citas_semana:
        cita.repuestos_usados = list(cita.repuestos_usados.all())
'''

content = content.replace("citas_semana = Cita.objects.filter(tecnico=request.user, fecha__range=[inicio_semana, fin_semana]).order_by('fecha', 'hora_inicio')", 
    "citas_semana = Cita.objects.filter(tecnico=request.user, fecha__range=[inicio_semana, fin_semana]).order_by('fecha', 'hora_inicio')" + new_data)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)

path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_agenda.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    content_html = f.read()

new_cita_data = '''
        estado:       "{{ cita.estado.nombre|escapejs }}",
        observaciones:"{{ cita.observaciones|default:''|escapejs }}",
        repuestos: [
            {% for inv in cita.repuestos_usados %}
            { id: "{{ inv.id }}", nombre: "{{ inv.repuesto.nombre|escapejs }}", cantidad: {{ inv.cantidad }} }{% if not forloop.last %},{% endif %}
            {% endfor %}
        ]
    }'''

content_html = re.sub(r'estado:\s*"\{\{ cita.estado.nombre\|escapejs \}\}",\s*observaciones:"\{\{ cita.observaciones\|default:\'\'\|escapejs \}\}"\s*\}', new_cita_data, content_html, flags=re.DOTALL)

with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(content_html)

print('Updated dashboard_views and template with repuestos data')
