from django.shortcuts import render

def seleccionar_dispositivo(request):
    return render(request, 'citas/seleccionar_dispositivo.html')