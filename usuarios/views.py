from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def auth_view(request):
    """Vista unificada de login y registro"""

    # -- PROCESAR LOGIN --
    if request.method == 'POST' and 'login_submit' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('agendamiento')  # Redirige al inicio tras login
        else:
            return render(request, 'usuarios/auth.html', {
                'error_login': 'Usuario o contraseña incorrectos. Intenta de nuevo.'
            })

    # -- PROCESAR REGISTRO --
    if request.method == 'POST' and 'registro_submit' in request.POST:
        nombre = request.POST.get('nombre', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/auth.html', {
                'error_registro': 'Ese nombre de usuario ya está en uso. Elige otro.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre.split()[0] if nombre else '',
            last_name=' '.join(nombre.split()[1:]) if nombre else '',
        )
        login(request, user)
        return redirect('agendamiento')

    # -- GET: mostrar el formulario --
    return render(request, 'usuarios/auth.html')


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('login')