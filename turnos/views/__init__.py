from .auth_views import RegistroView, CustomLoginView, home
from .agendamiento_views import (
    seleccionar_dispositivo,
    seleccionar_servicio,
    seleccionar_fecha_hora,
    resumen_cita,
    cita_confirmada,
    detalle_cita,
    ver_turno,
    notificar_retraso
)
from .dashboard_views import (
    # Admin
    admin_dashboard,
    admin_usuarios,
    admin_crear_usuario,
    admin_editar_usuario,
    admin_toggle_usuario,
    admin_servicios,
    admin_crear_servicio,
    admin_editar_servicio,
    admin_toggle_servicio,
    admin_citas,
    admin_reportes,
    admin_tecnicos,
    admin_inventario,
    # Técnico
    dashboard_tecnico,
    tecnico_agenda,
    tecnico_dispositivos,
    tecnico_clientes,
    tecnico_soporte,
    tecnico_reporte_mensual,
    tecnico_perfil,
    exportar_inventario_excel,
    agregar_repuesto,
    # Cliente
    cliente_inicio,
    cliente_servicios,
    cliente_perfil,
    cliente_soporte,
)
