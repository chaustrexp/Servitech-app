# Especificaciones de Casos de Uso - ServiTech

Documento oficial de especificaciones de casos de uso para la plataforma de gestión técnica **ServiTech**.

---

## 📋 Módulo 1: Inicio / Dashboard

### CU01 - Visualizar Resumen Operativo del Dashboard

| Campo | Detalle |
|---|---|
| **ID-CU** | CU01 |
| **Nombre CU** | Visualizar Resumen Operativo del Dashboard |
| **Descripción** | Permite al usuario consultar el estado general del sistema, KPIs en tiempo real y métricas del día según su rol. |
| **Actor** | Administrador / Técnico |
| **Precondiciones** | El usuario debe haber iniciado sesión en la plataforma con credenciales válidas. |
| **Flujo normal** | 1. El usuario ingresa a la aplicación o selecciona la opción "Inicio" del menú.<br>2. El sistema identifica el rol del usuario.<br>3. El sistema realiza la carga de las tarjetas de métricas y resumen operativo.<br>4. El sistema despliega el Dashboard con los datos e indicadores actualizados. |
| **Postcondiciones** | El usuario visualiza la información contextualizada del estado operativo del sistema. |
| **Flujos alternativos** | 3a. Error en la carga de datos: El sistema muestra un mensaje emergente de reconexión y mantiene la última vista almacenada en caché. |
| **Flujo principal** | Autenticación de usuario -> Selección del módulo Inicio -> Consulta de indicadores generales -> Renderizado del panel general. |

---

## 📋 Módulo 2: Citas y Agendamiento

### CU02 - Agendar Cita de Servicio Técnico

| Campo | Detalle |
|---|---|
| **ID-CU** | CU02 |
| **Nombre CU** | Agendar Cita de Servicio Técnico |
| **Descripción** | Proceso mediante el cual un cliente selecciona el tipo de equipo, servicio requerido y reserva un horario disponible. |
| **Actor** | Cliente |
| **Precondiciones** | El servicio deseado debe estar activo en el catálogo del sistema. |
| **Flujo normal** | 1. El cliente selecciona la opción "Nueva Cita".<br>2. El cliente selecciona el tipo de dispositivo a reparar o revisar.<br>3. El cliente elige el servicio técnico del catálogo.<br>4. El sistema despliega las fechas y franjas horarias disponibles.<br>5. El cliente selecciona fecha, hora y confirma la reserva.<br>6. El sistema guarda la cita y genera una confirmación en pantalla. |
| **Postcondiciones** | La cita queda registrada en estado "Pendiente" y asignada al flujo de atención. |
| **Flujos alternativos** | 5a. La franja horaria es reservada simultáneamente por otro cliente: El sistema notifica la indisponibilidad y solicita elegir otro horario. |
| **Flujo principal** | Selección de dispositivo -> Selección de servicio -> Elección de fecha y hora -> Registro de datos del cliente -> Confirmación de reserva. |

### CU03 - Administrar Estado y Demoras de Citas

| Campo | Detalle |
|---|---|
| **ID-CU** | CU03 |
| **Nombre CU** | Administrar Estado y Demoras de Citas |
| **Descripción** | Permite gestionar el estado de las citas (confirmar, reprogramar, cancelar) y notificar imprevistos o demoras al cliente. |
| **Actor** | Técnico / Administrador |
| **Precondiciones** | Debe existir al menos una cita registrada en el sistema. |
| **Flujo normal** | 1. El actor ingresa al módulo "Citas" o "Mi Agenda".<br>2. El sistema muestra el listado de citas registradas.<br>3. El actor selecciona una cita específica.<br>4. El actor actualiza el estado o pulsa la opción "Notificar Demora".<br>5. El actor ingresa el tiempo estimado de retraso y el motivo.<br>6. El sistema actualiza la cita y envía la notificación de contingencia. |
| **Postcondiciones** | El nuevo estado o aviso de contingencia queda registrado en la orden de servicio. |
| **Flujos alternativos** | 4a. El cliente solicita cancelación: El actor selecciona "Cancelar Cita", el sistema libera el cupo en el calendario operativo. |
| **Flujo principal** | Búsqueda/Filtro de cita -> Selección del registro -> Aplicación del cambio de estado o novedad -> Emisión de alerta al cliente. |

---

## 📋 Módulo 3: Técnicos

### CU04 - Controlar Estado de Turno Técnico

| Campo | Detalle |
|---|---|
| **ID-CU** | CU04 |
| **Nombre CU** | Controlar Estado de Turno Técnico |
| **Descripción** | Permite a los técnicos cambiar su estado operativo (Disponible, En Servicio, Pausar Turno) durante la jornada laboral. |
| **Actor** | Técnico |
| **Precondiciones** | El técnico debe tener la sesión activa en el panel. |
| **Flujo normal** | 1. El técnico visualiza su indicador de estado en la barra lateral o panel.<br>2. El técnico hace clic en la acción "Pausar Turno" o cambiar estado.<br>3. El sistema valida que el técnico no tenga servicios asignados en ejecución en ese instante.<br>4. El sistema actualiza el indicador a "En Pausa" / "No Disponible". |
| **Postcondiciones** | El sistema no asigna nuevas citas automáticas mientras el técnico se encuentre en pausa. |
| **Flujos alternativos** | 3a. El técnico tiene un servicio activo: El sistema muestra un mensaje requiriendo finalizar la orden actual antes de pausar el turno. |
| **Flujo principal** | Consulta de disponibilidad actual -> Solicitud de cambio de estado -> Verificación de carga laboral -> Actualización de la regla de asignación. |

---

## 📋 Módulo 5: Catálogo de Servicios

### CU05 - Gestionar Oferta de Servicios y SLA

| Campo | Detalle |
|---|---|
| **ID-CU** | CU05 |
| **Nombre CU** | Gestionar Oferta de Servicios y SLA |
| **Descripción** | Permite registrar, editar precios, tiempos estimados de atención y configurar acuerdos de nivel de servicio (SLA). |
| **Actor** | Administrador |
| **Precondiciones** | Contar con permisos de administración general. |
| **Flujo normal** | 1. El administrador ingresa al módulo "Catálogo".<br>2. El sistema despliega la lista de servicios activos e inactivos.<br>3. El administrador selecciona "Nuevo Servicio" o edita uno existente.<br>4. El administrador especifica nombre, costo base, tiempo estimado y conmutador SLA.<br>5. El administrador guarda los cambios.<br>6. El sistema actualiza el catálogo global. |
| **Postcondiciones** | La oferta de servicios queda disponible e inmediatamente actualizada para las reservas de los clientes. |
| **Flujos alternativos** | 5a. Datos obligatorios incompletos: El sistema resalta los campos faltantes y no permite guardar hasta corregir. |
| **Flujo principal** | Apertura del catálogo -> Formulario de parámetros del servicio -> Ajuste de niveles SLA -> Confirmación y publicación. |

---

## 📋 Módulo 6: Reportes

### CU06 - Exportar Informe Analítico en PDF

| Campo | Detalle |
|---|---|
| **ID-CU** | CU06 |
| **Nombre CU** | Exportar Informe Analítico en PDF |
| **Descripción** | Genera y descarga un informe ejecutivo con indicadores de rendimiento, tiempos de respuesta y valoración de clientes en formato PDF. |
| **Actor** | Administrador |
| **Precondiciones** | Debe haber datos registrados dentro del rango de fechas seleccionado (Mensual / Anual). |
| **Flujo normal** | 1. El administrador ingresa al módulo "Reportes".<br>2. El administrador ajusta el conmutador de periodo (Mensual o Anual).<br>3. El administrador hace clic en el botón "Exportar Reporte".<br>4. El sistema procesa las métricas mediante la librería client-side (jsPDF / AutoTable).<br>5. El navegador descarga automáticamente el documento en formato PDF con diseño ejecutivo y membrete corporativo. |
| **Postcondiciones** | Se obtiene el archivo PDF estructurado listo para impresión o auditoría. |
| **Flujos alternativos** | 2a. No existen registros en el período seleccionado: El sistema muestra un aviso de alerta indicando "Sin datos para exportar". |
| **Flujo principal** | Filtrado del rango analítico -> Agrupación de datos operativos -> Renderizado del archivo vectorial -> Descarga del documento PDF. |

---

## 📋 Módulo 7: Inventario

### CU07 - Controlar Stock Crítico y Exportar Inventario a Excel

| Campo | Detalle |
|---|---|
| **ID-CU** | CU07 |
| **Nombre CU** | Controlar Stock Crítico y Exportar Inventario a Excel |
| **Descripción** | Monitoreo del stock de repuestos técnicos, visualización de barras de progreso, alertas de stock bajo y exportación a Excel. |
| **Actor** | Administrador / Técnico |
| **Precondiciones** | Existencia del módulo de componentes y repuestos configurado. |
| **Flujo normal** | 1. El usuario accede a la sección "Inventario".<br>2. El sistema calcula el porcentaje de stock de cada repuesto e ilustra mediante barras de progreso visuales.<br>3. El sistema resalta en rojo las tarjetas de componentes marcados con "Stock Crítico".<br>4. El usuario selecciona el botón "Exportar".<br>5. El sistema procesa los datos mediante ExcelJS y descarga la plantilla organizada de inventario. |
| **Postcondiciones** | El usuario descarga la hoja de cálculo con el consolidado del inventario técnico. |
| **Flujos alternativos** | 3a. El usuario presiona "Crear Orden" en los suministros sugeridos: El sistema simula la solicitud de compra y despliega una notificación Toast de confirmación en pantalla. |
| **Flujo principal** | Lectura de existencias físicas -> Identificación de alertas por nivel mínimo -> Formateo de dataset -> Exportación en hoja de cálculo. |