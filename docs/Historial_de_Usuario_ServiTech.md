# 📱 ServiTech - Sistema de Agendamiento y Gestión de Turnos Digitales
## Especificación Funcional de Historiales de Usuario (User Stories)

> **Documento generado a partir del archivo:** `Historial de Usuario ServiTech.xlsx`  
> **Estructura de origen:** Libro de Excel con múltiples hojas divididas por módulos funcionales.  
> **Fecha de consolidación:** Julio 2026  

---

## 📋 Tabla de Contenidos y Resumen por Módulo

| Módulo | Nombre del Módulo | Hojas de Origen | Historiales de Usuario (HU) | Actores Principales |
| :--- | :--- | :--- | :--- | :--- |
| **Módulo 1** | [Agendamiento (Cliente Final)](#módulo-1-agendamiento--cliente-final-) | `Módulo 1` | HU-01, HU-02 | Cliente final |
| **Módulo 2** | [Manejo de Contingencias e Imprevistos](#módulo-2-manejo-de-contingencias-e-imprevistos--cliente--técnico-) | `Módulo 2` | HU-03, HU-04, HU-05 | Cliente, Técnico |
| **Módulo 3** | [Dashboard y Gestión Operativa](#módulo-3-dashboard-y-gestión-operativa--técnico--recepción-) | `Módulo 3` | HU-06, HU-07 | Técnico, Recepcionista |
| **Módulo 4** | [Administración y Configuración](#módulo-4-administración-y-configuración--administrador-) | `Módulo 4` | HU-08 | Administrador |

---

## 📌 Módulo 1: Agendamiento ( Cliente Final )
> **Hoja de origen:** `Módulo 1`  
> **Objetivo del módulo:** Permitir a los clientes finales seleccionar el tipo de servicio, dispositivo, técnico de preferencia y bloque horario de manera autónoma y fluida.

### 🔹 HU-01: Selección de Dispositivo y Tipo de Cita

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-01` |
| **Módulo** | Módulo 1: Agendamiento |
| **👤 Como (Actor)** | Cliente final |
| **🎯 Quiero (Acción)** | Seleccionar el tipo de dispositivo (Celular / Laptop / PC) y el motivo de la cita (Diagnóstico, Reparación Exprés, Entrega, Garantía, Asesoría). |
| **💡 Para (Beneficio)** | Que el sistema me asigne el tiempo adecuado y el personal capacitado. |

#### ✅ Criterios de Aceptación
1. **Listado claro con duraciones:** Debe mostrar una lista clara de servicios con su duración estimada.
2. **Obligatoriedad del paso:** Debe ser un paso obligatorio antes de ver los horarios disponibles.

---

### 🔹 HU-02: Visualización de Bloques Libres y Elección de Técnico

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-02` |
| **Módulo** | Módulo 1: Agendamiento |
| **👤 Como (Actor)** | Cliente final |
| **🎯 Quiero (Acción)** | Visualizar los bloques de tiempo libres y, opcionalmente, elegir a mi técnico de preferencia. |
| **💡 Para (Beneficio)** | Agendar en el momento que mejor se adapte a mi disponibilidad. |

#### ✅ Criterios de Aceptación
1. **Filtro por técnico específico:** Si elijo un técnico específico, la agenda se filtra únicamente con sus turnos disponibles.
2. **Vista global ("Cualquier técnico"):** Si selecciono *"Cualquier técnico"*, el sistema muestra todos los espacios libres del taller de forma consolidada.

---

## 📌 Módulo 2: Manejo de Contingencias e Imprevistos ( Cliente / Técnico )
> **Hoja de origen:** `Módulo 2`  
> **Objetivo del módulo:** Gestionar las variaciones en tiempo real (retrasos, cancelaciones y extensiones de reparación) para mantener sincronizadas las agendas del taller y los clientes.

### 🔹 HU-03: Notificación de Retraso por Parte del Cliente

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-03` |
| **Módulo** | Módulo 2: Contingencias e Imprevistos |
| **👤 Como (Actor)** | Cliente que tiene una cita agendada |
| **🎯 Quiero (Acción)** | Presionar un botón de **"Llegaré tarde (+10 / +15 min)"** desde el recordatorio recibido. |
| **💡 Para (Beneficio)** | Avisar al taller y evitar que cancelen mi cupo automáticamente. |

#### ✅ Criterios de Aceptación
1. **Acceso directo sin autenticación compleja:** La acción se debe realizar mediante un enlace seguro sin necesidad de iniciar sesión.
2. **Actualización en tiempo real:** El estado de la cita cambia automáticamente a **"Retrasado con Aviso"** en el panel del técnico.

---

### 🔹 HU-04: Reagendamiento o Cancelación en 1 Clic

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-04` |
| **Módulo** | Módulo 2: Contingencias e Imprevistos |
| **👤 Como (Actor)** | Cliente que no puede asistir |
| **🎯 Quiero (Acción)** | Cancelar o reprogramar mi cita desde el mensaje de confirmación/recordatorio. |
| **💡 Para (Beneficio)** | Liberar el turno para otra persona y no hacer perder tiempo al técnico. |

#### ✅ Criterios de Aceptación
1. **Cancelación con motivo:** Permite indicar la razón de la cancelación de forma rápida.
2. **Notificación de respaldo:** Se genera y envía una confirmación formal de la cancelación al cliente.

---

### 🔹 HU-05: Ajuste de Agenda por Reparación Extendida

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-05` |
| **Módulo** | Módulo 2: Contingencias e Imprevistos |
| **👤 Como (Actor)** | Técnico de reparación |
| **🎯 Quiero (Acción)** | Marcar **"Diagnóstico/Reparación Extendida (+15 min)"** en mi panel cuando una revisión tome más tiempo del previsto. |
| **💡 Para (Beneficio)** | Que el sistema notifique automáticamente al siguiente cliente sobre el ajuste en la hora de su atención. |

#### ✅ Criterios de Aceptación
1. **Alerta preventiva al cliente subsecuente:** El sistema envía un mensaje/alerta al cliente de la siguiente cita informando el ligero desplazamiento.
2. **Desplazamiento dinámico de agenda:** La agenda del día del técnico se desplaza dinámicamente en cascada conforme va terminando cada tarea.

---

## 📌 Módulo 3: Dashboard y Gestión Operativa ( Técnico / Recepción )
> **Hoja de origen:** `Módulo 3`  
> **Objetivo del módulo:** Proporcionar al personal operativo del taller herramientas de control en tiempo real para gestionar el flujo diario de atención y ausencias.

### 🔹 HU-06: Panel de Citas del Día (Dashboard Técnico)

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-06` |
| **Módulo** | Módulo 3: Dashboard Técnico |
| **👤 Como (Actor)** | Técnico / Operador |
| **🎯 Quiero (Acción)** | Ver la lista cronológica de mis citas del día con el estado actual (*Confirmada, En Diagnóstico, Retrasada, Finalizada*). |
| **💡 Para (Beneficio)** | Organizar mi mesa de trabajo y atender a los clientes a tiempo. |

#### ✅ Criterios de Aceptación
1. **Cambio de estado ágil:** Permite cambiar el estado de la cita mediante un switch de estados de interfaz intuitiva.
2. **Indicadores visuales de alerta:** Muestra iconos de alerta visibles si un cliente avisó que viene con retraso.

---

### 🔹 HU-07: Liberación por No-Show (Cliente Ausente)
> *(Nota aclaratoria de origen: En el archivo Excel original aparece subtitulado como "Módulo 2 HU-07", pero se encuentra ubicado y clasificado lógicamente dentro de la hoja del **Módulo 3**).*

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-07` |
| **Módulo** | Módulo 3: Dashboard Operativo / Recepción |
| **👤 Como (Actor)** | Recepcionista / Técnico |
| **🎯 Quiero (Acción)** | Marcar una cita como **No-Show** si han pasado más de 10-15 minutos de tolerancia sin reporte del cliente. |
| **💡 Para (Beneficio)** | Liberar el espacio y atender a clientes presenciales sin cita (*walk-ins*). |

#### ✅ Criterios de Aceptación
1. **Confirmación de seguridad:** Muestra una advertencia antes de confirmar el cambio de estado para evitar cancelaciones accidentales.
2. **Reapertura de cupo:** El espacio en la agenda vuelve a aparecer como disponible en el sistema para nuevas asignaciones.

---

## 📌 Módulo 4: Administración y Configuración ( Administrador )
> **Hoja de origen:** `Módulo 4`  
> **Objetivo del módulo:** Permitir a la administración del taller parametrizar el catálogo de servicios, tiempos operativos, holguras (*buffers*) y especialidades.

### 🔹 HU-08: Gestión de Catálogo de Servicios y Duración

| Elemento | Detalle |
| :--- | :--- |
| **Código** | `HU-08` |
| **Módulo** | Módulo 4: Administración |
| **👤 Como (Actor)** | Administrador del taller |
| **🎯 Quiero (Acción)** | Crear, editar y parametrizar los tipos de citas y sus duraciones estimadas. |
| **💡 Para (Beneficio)** | Ajustar la lógica de tiempos de la plataforma a las capacidades reales de mi taller. |

#### ✅ Criterios de Aceptación
1. **Parametrización completa:** Permite definir la duración en minutos, el margen de amortiguación (*buffer* de tiempo entre citas) y la especialidad requerida para cada servicio.

---

## 📊 Matriz de Trazabilidad de Requerimientos (Resumen Consolidado)

| Código | Hoja Excel | Módulo | Actor | Descripción Corta | Criterios Clave |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **HU-01** | `Módulo 1` | Agendamiento | Cliente final | Selección de dispositivo y tipo de cita | Lista de servicios con duración; paso obligatorio |
| **HU-02** | `Módulo 1` | Agendamiento | Cliente final | Selección de bloques libres y técnico | Filtro por técnico o vista global |
| **HU-03** | `Módulo 2` | Contingencias | Cliente agendado | Aviso de retraso (+10/+15 min) | Enlace seguro sin login; estado "Retrasado con Aviso" |
| **HU-04** | `Módulo 2` | Contingencias | Cliente agendado | Reagendamiento / Cancelación rápida | Cancelación con motivo; confirmación automática |
| **HU-05** | `Módulo 2` | Contingencias | Técnico | Ajuste por reparación extendida (+15 min) | Alerta al cliente siguiente; desplazamiento dinámico |
| **HU-06** | `Módulo 3` | Dashboard | Técnico / Operador | Panel del día y cambio de estados | Switch de estados; iconos de alerta |
| **HU-07** | `Módulo 3` | Dashboard | Recepción / Técnico | Liberación de cupo por No-Show | Advertencia previa; espacio liberado para walk-ins |
| **HU-08** | `Módulo 4` | Administración | Administrador | Catálogo de servicios y duraciones | Duración, buffer y especialidad técnica |

---
*Fin del documento - Especificación ServiTech*
