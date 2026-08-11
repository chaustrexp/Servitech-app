import os
import re

admin_path = r"c:\Servitech\Servitech-app\turnos\templates\turnos\administracion\admin_citas.html"
tecnico_path = r"c:\Servitech\Servitech-app\turnos\templates\turnos\tecnico\tecnico_historial.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Base template
content = content.replace("{% extends 'turnos/administracion/admin_base.html' %}", "{% extends 'turnos/tecnico/tecnico_base.html' %}")

# 2. Title
content = content.replace("Gestión de Citas - Panel de Administración", "Mi Historial - Panel del Técnico")

# 3. Form action
content = content.replace("{% url 'admin_citas' %}", "{% url 'tecnico_historial' %}")

# 4. Remove Técnico Filter block
tecnico_filter_regex = r'<!-- Filtro Técnico -->.*?</div>\s*</div>\s*</div>'
content = re.sub(tecnico_filter_regex, '', content, flags=re.DOTALL)

# Also fix the grid-cols of filters from 5 to 4 so it spans correctly (optional, but 4 is better if we remove one)
content = content.replace("lg:grid-cols-5", "lg:grid-cols-4")

# 5. Remove Técnico table header
content = content.replace('<th class="py-4 px-6">Técnico</th>', '')

# 6. Remove Técnico table body column
tecnico_tbody_regex = r'<!-- Técnico -->.*?</td>'
content = re.sub(tecnico_tbody_regex, '', content, flags=re.DOTALL)

# 7. Remove Técnico from mobile view
mobile_tecnico_regex = r'<p><strong>Técnico:</strong> {{ cita\.tecnico\.nombre_completo\|default:"Sin asignar" }}</p>'
content = re.sub(mobile_tecnico_regex, '', content)

# 8. Pagination links
content = content.replace("{% if request.GET.tecnico %}&tecnico={{ request.GET.tecnico }}{% endif %}", "")

# 9. Excel export URL
content = content.replace("{% url 'admin_exportar_citas_excel' %}", "{% url 'exportar_historial_excel' %}")

# 10. Heading
content = content.replace("Listado de Citas", "Mi Historial de Citas")

with open(tecnico_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template creado con éxito.")
