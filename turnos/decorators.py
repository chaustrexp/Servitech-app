from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models.usuarios import Usuario
from django.http import JsonResponse

def rol_requerido(roles_permitidos):
    """
    Decorador para verificar que el usuario tenga un rol específico.
    Si no tiene el rol y no es administrador, se le deniega el acceso.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
                return redirect('login')
                
            if request.user.es_admin:
                return view_func(request, *args, **kwargs)
                
            if request.user.rol not in roles_permitidos:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
                raise PermissionDenied("No tienes permisos para acceder a esta sección.")
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
