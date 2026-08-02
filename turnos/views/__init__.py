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
    admin_dashboard,
    dashboard_tecnico,
    tecnico_agenda,
    tecnico_dispositivos,
    tecnico_clientes,
    tecnico_soporte,
    tecnico_reporte_mensual,
    cliente_inicio,
    cliente_servicios,
    cliente_perfil,
    cliente_soporte,
    tecnico_perfil,
    exportar_inventario_excel,
    agregar_repuesto
)

