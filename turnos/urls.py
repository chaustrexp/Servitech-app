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

    # ── Dashboards ────────────────────────────────────────────────
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),

    # ── Turnos Digitales ──────────────────────────────────────────
    path('turno/<int:turno_id>/', views.ver_turno, name='ver_turno'),
    path('turno/<int:turno_id>/retraso/', views.notificar_retraso, name='notificar_retraso'),
]