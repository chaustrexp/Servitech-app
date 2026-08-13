# 🛠️ Servitech App

Plataforma web diseñada para la gestión integral de servicios técnicos, agendamiento de citas y control de mantenimiento. El sistema conecta de forma eficiente a clientes, personal técnico y administradores.

---

## 👥 Roles de Usuario

| Rol | Descripción |
|-----|-------------|
| 🧑‍💻 **Cliente** | Agenda citas, consulta servicios y hace seguimiento a sus solicitudes. |
| 🔧 **Técnico** | Gestiona órdenes de trabajo, historial de atenciones y diagnósticos. |
| 🛡️ **Administrador** | Control total de usuarios, citas, reportes, inventario y auditoría. |

---

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.12 / Django 6.0
- **Frontend:** HTML5, Tailwind CSS, JavaScript, Chart.js
- **Base de Datos:** PostgreSQL (recomendado) / SQLite
- **Exportaciones:** Excel (`openpyxl`) y PDF (`reportlab`) server-side
- **Control de Versiones:** Git & GitHub

---

## ✨ Novedades Recientes

### 🔒 Sistema de Auditoría (triggers PostgreSQL)
Se implementó una tabla `auditoria_log` con triggers nativos de PostgreSQL que registran automáticamente cada `INSERT`, `UPDATE` y `DELETE` sobre las tablas de:
- **Citas** (`turnos_cita`)
- **Clientes / Usuarios** (`turnos_usuario`) — etiquetas `clientes` y `personas`
- **Sesiones** (`django_session`)

Cada registro guarda: tabla, operación, ID afectado, datos anteriores/nuevos (JSONB), usuario de BD, IP y timestamp.
Visible en el admin de Django en `/admin/turnos/auditorialog/` (solo lectura).

### 📄 Exportar Reportes a PDF
El botón **"Exportar PDF"** en la sección de Reportes Analíticos ahora genera un PDF completo server-side con `reportlab`, incluyendo:
- KPIs del mes (citas, finalizadas, canceladas, tasa de éxito)
- Servicios más solicitados
- Técnicos con más atenciones
- Tabla de atenciones recientes

### 📦 Modelo de Dispositivos
Se agregó el modelo `Dispositivo` y su migración `0012`, permitiendo asociar dispositivos a citas.

---

## 🚀 Instalación y Configuración Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/chaustrexp/Servitech-app.git
cd Servitech-app
```

### 2. Crear y activar el entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto (junto a `manage.py`):

```env
USE_POSTGRES=True
DB_NAME=servitech
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=localhost
DB_PORT=5432
```

> Asegúrate de haber creado previamente la base de datos `servitech` en PostgreSQL.

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

Esto también instalará automáticamente los **triggers de auditoría** en PostgreSQL.

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Levantar el servidor
```bash
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador.

---

## 🧪 Datos de Prueba

Para vaciar la base de datos y generar datos de prueba:

> ⚠️ **Advertencia:** Esto eliminará todos los datos actuales.

```bash
python manage.py flush --no-input
python seed_full.py
```

**Scripts automáticos:**
- **Windows:** `reset_db.bat`
- **macOS/Linux:** `./reset_db.sh`

### Limpieza de tablas manuales (solo pgAdmin)
Si existen tablas creadas manualmente que no tengan prefijo `turnos_`, `auth_` o `django_`, elimínalas antes de migrar:

```sql
DROP TABLE IF EXISTS
    historial_cita, notificacion, horario_tecnico,
    cita, servicio, estado_cita, especialidad, usuario
CASCADE;
```

---

## 💡 Solución a Errores Comunes

### `ModuleNotFoundError: No module named 'dotenv'`
El entorno virtual no está activo. En PowerShell usa:
```powershell
venv\Scripts\Activate.ps1
```
O ejecuta directamente sin activar:
```powershell
venv\Scripts\python manage.py runserver
```

### `ProgrammingError: no existe la relación 'auth_user'`
El proyecto usa un modelo de usuario personalizado (`turnos_usuario`). Asegúrate de aplicar todas las migraciones con `python manage.py migrate` antes de cualquier operación.
