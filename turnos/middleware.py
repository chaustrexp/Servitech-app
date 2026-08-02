from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings


class RoleSessionMiddleware(SessionMiddleware):
    """
    Middleware personalizado que asigna cookies de sesión independientes
    según el portal activo (Cliente, Técnico o Admin).
    
    Permite mantener sesiones simultáneas en pestañas distintas del mismo navegador.
    Al cerrar la pestaña/navegador, la sesión expira gracias a SESSION_EXPIRE_AT_BROWSER_CLOSE=True.
    
    Estrategia: modificamos temporalmente settings.SESSION_COOKIE_NAME antes de llamar
    al middleware padre, para que toda la lógica de sesión (save, CSRF, etc.) use el
    nombre correcto sin reimplementarla.
    """

    def _get_cookie_name(self, request):
        """Determina el nombre de cookie correcto según la ruta o el parámetro role_context."""
        path = request.path_info

        # 1. Rutas de portales específicos
        if path.startswith('/tecnico'):
            return 'sessionid_tecnico'
        if path.startswith('/cliente'):
            return 'sessionid_cliente'
        if path.startswith('/administracion') or path.startswith('/admin'):
            return 'sessionid_admin'

        # 2. Rutas neutras: /login/, /logout/, /registro/ — usar el parámetro role_context
        role_param = (
            request.POST.get('role_context')
            or request.GET.get('role_context')
        )
        if role_param == 'tecnico':
            return 'sessionid_tecnico'
        if role_param in ('cliente', 'recepcionista'):
            return 'sessionid_cliente'
        if role_param == 'admin':
            return 'sessionid_admin'

        # 3. Inferir por el Referer (útil en POST del login)
        referer = request.META.get('HTTP_REFERER', '')
        if '/tecnico' in referer:
            return 'sessionid_tecnico'
        if '/cliente' in referer:
            return 'sessionid_cliente'
        if '/administracion' in referer:
            return 'sessionid_admin'

        # 4. Fallback: cookie estándar
        return settings.SESSION_COOKIE_NAME

    def process_request(self, request):
        """Inyecta el nombre de cookie correcto antes de cargar la sesión."""
        cookie_name = self._get_cookie_name(request)
        # Guardamos el nombre en el request para usarlo en process_response
        request._role_session_cookie_name = cookie_name

        # Temporalmente ajustamos el nombre para que el padre lea la cookie correcta
        original = settings.SESSION_COOKIE_NAME
        settings.SESSION_COOKIE_NAME = cookie_name
        try:
            super().process_request(request)
        finally:
            settings.SESSION_COOKIE_NAME = original

    def process_response(self, request, response):
        """Guarda la sesión con el nombre de cookie correcto."""
        cookie_name = getattr(request, '_role_session_cookie_name', settings.SESSION_COOKIE_NAME)

        original = settings.SESSION_COOKIE_NAME
        settings.SESSION_COOKIE_NAME = cookie_name
        try:
            response = super().process_response(request, response)
        finally:
            settings.SESSION_COOKIE_NAME = original

        return response
