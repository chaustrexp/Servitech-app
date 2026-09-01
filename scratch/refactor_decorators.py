import re
import os

filepath = r"c:\django\Servitech-app\turnos\views\dashboard_views.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Añadir el import al principio si no existe
if 'from turnos.decorators import rol_requerido' not in content:
    content = content.replace("from django.contrib.auth.decorators import login_required", 
                              "from django.contrib.auth.decorators import login_required\nfrom turnos.decorators import rol_requerido")

# Lista de reemplazos para ADMINISTRADOR
admin_pattern = re.compile(
    r'@login_required\s*\n\s*def (\w+)\(request.*?\):\s*\n(?:\s*"""[\s\S]*?"""\s*\n)?\s*if request\.user\.rol != Usuario\.Rol\.ADMINISTRADOR:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n'
)

def admin_replacer(match):
    full_match = match.group(0)
    # Reemplazar @login_required con @login_required + @rol_requerido
    new_str = re.sub(
        r'@login_required',
        r'@login_required\n@rol_requerido([Usuario.Rol.ADMINISTRADOR])',
        full_match
    )
    # Remover el if
    new_str = re.sub(
        r'\s*if request\.user\.rol != Usuario\.Rol\.ADMINISTRADOR:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n',
        '\n',
        new_str
    )
    return new_str

content = admin_pattern.sub(admin_replacer, content)

# Lista de reemplazos para TECNICO
tecnico_pattern = re.compile(
    r'@login_required\s*\n\s*def (\w+)\(request.*?\):\s*\n(?:\s*"""[\s\S]*?"""\s*\n)?\s*if request\.user\.rol != Usuario\.Rol\.TECNICO:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n'
)

def tecnico_replacer(match):
    full_match = match.group(0)
    new_str = re.sub(
        r'@login_required',
        r'@login_required\n@rol_requerido([Usuario.Rol.TECNICO])',
        full_match
    )
    new_str = re.sub(
        r'\s*if request\.user\.rol != Usuario\.Rol\.TECNICO:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n',
        '\n',
        new_str
    )
    return new_str

content = tecnico_pattern.sub(tecnico_replacer, content)

# Lista de reemplazos para CLIENTE
cliente_pattern = re.compile(
    r'@login_required\s*\n\s*def (\w+)\(request.*?\):\s*\n(?:\s*"""[\s\S]*?"""\s*\n)?\s*if request\.user\.rol != Usuario\.Rol\.CLIENTE:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n'
)

def cliente_replacer(match):
    full_match = match.group(0)
    new_str = re.sub(
        r'@login_required',
        r'@login_required\n@rol_requerido([Usuario.Rol.CLIENTE])',
        full_match
    )
    new_str = re.sub(
        r'\s*if request\.user\.rol != Usuario\.Rol\.CLIENTE:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n',
        '\n',
        new_str
    )
    return new_str

content = cliente_pattern.sub(cliente_replacer, content)

# There is also one specific for multiple roles:
# if request.user.rol not in [Usuario.Rol.TECNICO, Usuario.Rol.ADMINISTRADOR]:
multi_pattern = re.compile(
    r'@login_required\s*\n\s*def (\w+)\(request.*?\):\s*\n(?:\s*"""[\s\S]*?"""\s*\n)?\s*if request\.user\.rol not in \[Usuario\.Rol\.TECNICO, Usuario\.Rol\.ADMINISTRADOR\]:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n'
)
def multi_replacer(match):
    full_match = match.group(0)
    new_str = re.sub(
        r'@login_required',
        r'@login_required\n@rol_requerido([Usuario.Rol.TECNICO, Usuario.Rol.ADMINISTRADOR])',
        full_match
    )
    new_str = re.sub(
        r'\s*if request\.user\.rol not in \[Usuario\.Rol\.TECNICO, Usuario\.Rol\.ADMINISTRADOR\]:\s*\n\s*return (?:redirect\(\'home\'\)|JsonResponse.*?)\s*\n',
        '\n',
        new_str
    )
    return new_str

content = multi_pattern.sub(multi_replacer, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Refactorización completada con éxito.")
