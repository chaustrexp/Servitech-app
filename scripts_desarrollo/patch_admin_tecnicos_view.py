import codecs
import re

path = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# Replace the password generation
old_pattern = r"pw_temporal = uuid\.uuid4\(\)\.hex\[:10\].*?password=pw_temporal,"
new_pattern = r'''password_nuevo = request.POST.get('password', '').strip()
                if not password_nuevo:
                    password_nuevo = uuid.uuid4().hex[:10]
                    
                tecnico = Usuario.objects.create_user(
                    correo=correo,
                    password=password_nuevo,'''

if re.search(old_pattern, content, re.DOTALL):
    content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(content)
    print('Patched successfully!')
else:
    print('Pattern not found')
