# Las vistas son la interface con el usuario

# La logica que procesa los datos para las interfaz


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Turno

# Muestra la interfaz del Turno Digital
def ver_turno(request, codigo_turno):
    turno = get_object_or_404(Turno, codigo_turno=codigo_turno)
    return render(request, 'turnos/turno_digital.html', {'turno': turno})

# Acción para notificar retraso (RF-04 con autenticación)
@login_required
def notificar_retraso(request, turno_id):
    if request.method == "POST":
        turno = get_object_or_404(Turno, id=turno_id, cliente=request.user)
        
        # Validar RN-03 (Límite de aviso único)
        if not turno.notifico_retraso:
            turno.notifico_retraso = True
            turno.minutos_retraso_notificados = 10
            turno.estado = 'RETRASADO_CON_AVISO'
            turno.save()
            
    return redirect('ver_turno', codigo_turno=turno.codigo_turno)

def seleccionar_dispositivo(request):
    return render(request, 'turnos/seleccionar_dipositivo.html')