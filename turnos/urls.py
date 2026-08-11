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

    # ── Dashboards Admin ──────────────────────────────────────────
    path('admin-panel/',                                    views.admin_dashboard,       name='admin_dashboard'),
    path('admin-panel/usuarios/',                           views.admin_usuarios,         name='admin_usuarios'),
    path('admin-panel/usuarios/exportar/',                  views.admin_exportar_usuarios_excel, name='admin_exportar_usuarios_excel'),
    path('admin-panel/usuarios/crear/',                     views.admin_crear_usuario,    name='admin_crear_usuario'),
    path('admin-panel/usuarios/<int:usuario_id>/editar/',   views.admin_editar_usuario,   name='admin_editar_usuario'),
    path('admin-panel/usuarios/<int:usuario_id>/toggle/',   views.admin_toggle_usuario,   name='admin_toggle_usuario'),
    path('admin-panel/servicios/',                          views.admin_servicios,        name='admin_servicios'),
    path('admin-panel/servicios/crear/',                    views.admin_crear_servicio,   name='admin_crear_servicio'),
    path('admin-panel/servicios/<int:servicio_id>/editar/', views.admin_editar_servicio,  name='admin_editar_servicio'),
    path('admin-panel/servicios/<int:servicio_id>/toggle/', views.admin_toggle_servicio,  name='admin_toggle_servicio'),
    path('admin-panel/citas/',                              views.admin_citas,            name='admin_citas'),
    path('admin-panel/citas/exportar/',                     views.admin_exportar_citas_excel, name='admin_exportar_citas_excel'),
    path('admin-panel/tecnicos/',                           views.admin_tecnicos,         name='admin_tecnicos'),
    path('admin-panel/reportes/',                           views.admin_reportes,         name='admin_reportes'),
    path('admin-panel/reportes/exportar/',                  views.admin_exportar_analitico_excel, name='admin_exportar_analitico_excel'),
    path('admin-panel/inventario/',                         views.admin_inventario,       name='admin_inventario'),
    path('admin-panel/inventario/historial/',               views.admin_historial_inventario, name='admin_historial_inventario'),
    path('admin-panel/perfil/',                             views.admin_perfil,           name='admin_perfil'),
    path('tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('tecnico/toggle-pausa/', views.tecnico_toggle_pausa, name='tecnico_toggle_pausa'),
    path('tecnico/agenda/', views.tecnico_agenda, name='tecnico_agenda'),
    path('tecnico/historial/', views.tecnico_historial, name='tecnico_historial'),
    path('tecnico/historial/exportar/', views.exportar_historial_excel, name='exportar_historial_excel'),
    path('tecnico/citas/<int:cita_id>/aceptar/', views.aceptar_cita, name='aceptar_cita'),
    path('tecnico/citas/<int:cita_id>/finalizar/', views.finalizar_cita, name='finalizar_cita'),
    path('tecnico/dispositivos/', views.tecnico_dispositivos, name='tecnico_dispositivos'),
    path('tecnico/clientes/historial-general/', views.tecnico_clientes_historial_general, name='tecnico_clientes_historial_general'),
    path('tecnico/clientes/', views.tecnico_clientes, name='tecnico_clientes'),
    path('tecnico/clientes/<int:cliente_id>/historial/', views.tecnico_cliente_historial, name='tecnico_cliente_historial'),
    path('tecnico/soporte/', views.tecnico_soporte, name='tecnico_soporte'),
    path('tecnico/reporte/', views.tecnico_reporte_mensual, name='tecnico_reporte_mensual'),
    path('tecnico/perfil/', views.tecnico_perfil, name='tecnico_perfil'),
    path('tecnico/inventario/exportar/', views.exportar_inventario_excel, name='exportar_inventario_excel'),

    path('cliente/inicio/', views.cliente_inicio, name='cliente_inicio'),
    path('cliente/servicios/', views.cliente_servicios, name='cliente_servicios'),
    path('cliente/soporte/', views.cliente_soporte, name='cliente_soporte'),
    path('cliente/perfil/', views.cliente_perfil, name='cliente_perfil'),

    # ── Turnos Digitales ──────────────────────────────────────────
    path('turno/<int:turno_id>/', views.ver_turno, name='ver_turno'),
    path('turno/<int:turno_id>/retraso/', views.notificar_retraso, name='notificar_retraso'),
]