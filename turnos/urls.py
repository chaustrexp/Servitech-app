from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # ── Raíz ──────────────────────────────────────────────────────
    path('', views.home, name='home'),

    # ── Autenticación ─────────────────────────────────────────────
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # ── Agendamiento ──────────────────────────────────────────────
    path('servicios/dispositivo/', views.seleccionar_dispositivo, name='seleccionar_dispositivo'),
    path('servicios/servicio/', views.seleccionar_servicio, name='seleccionar_servicio'),
    path('servicios/fecha-hora/', views.seleccionar_fecha_hora, name='seleccionar_fecha_hora'),
    path('servicios/resumen/', views.resumen_cita, name='resumen_cita'),
    path('cita/<int:cita_id>/confirmada/', views.cita_confirmada, name='cita_confirmada'),
    path('cita/<int:cita_id>/', views.detalle_cita, name='detalle_cita'),

    # ── Dashboards ────────────────────────────────────────────────
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('tecnico/agenda/', views.tecnico_agenda, name='tecnico_agenda'),
    path('tecnico/dispositivos/', views.tecnico_dispositivos, name='tecnico_dispositivos'),
    path('tecnico/clientes/', views.tecnico_clientes, name='tecnico_clientes'),
    path('tecnico/soporte/', views.tecnico_soporte, name='tecnico_soporte'),

    path('cliente/inicio/', views.cliente_inicio, name='cliente_inicio'),
    path('cliente/servicios/', views.cliente_servicios, name='cliente_servicios'),
    path('cliente/soporte/', views.cliente_soporte, name='cliente_soporte'),
    path('cliente/perfil/', views.cliente_perfil, name='cliente_perfil'),

    # ── Turnos Digitales ──────────────────────────────────────────
    path('turno/<int:turno_id>/', views.ver_turno, name='ver_turno'),
    path('turno/<int:turno_id>/retraso/', views.notificar_retraso, name='notificar_retraso'),
]