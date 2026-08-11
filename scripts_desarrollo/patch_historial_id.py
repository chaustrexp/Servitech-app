import codecs

# 1. Update HTML
path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/tecnico/tecnico_clientes.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    html = f.read()

html = html.replace('onclick="verHistorialCliente({{ cliente.id }}', 'onclick="verHistorialCliente({{ cliente.id_usuario }}')

with codecs.open(path_html, 'w', 'utf-8') as f:
    f.write(html)


# 2. Update views
path_views = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path_views, 'r', 'utf-8') as f:
    views = f.read()

views = views.replace('cliente = Usuario.objects.get(id=cliente_id, rol=Usuario.Rol.CLIENTE)', 'cliente = Usuario.objects.get(id_usuario=cliente_id, rol=Usuario.Rol.CLIENTE)')

with codecs.open(path_views, 'w', 'utf-8') as f:
    f.write(views)

print('Fixed ID issues in Historial del Cliente')
