# 🛠️ Servitech App

Plataforma web diseñada para la gestión integral de servicios técnicos, agendamiento de citas y control de mantenimiento. El sistema permite conectar de forma eficiente a clientes, personal técnico y administradores.

---

## 👥 Roles de Usuario y Funcionalidades

La aplicación está estructurada para dar soporte a tres perfiles principales:

* **🧑‍💻 Cliente:** Explora el catálogo de servicios, selecciona la fecha y hora de atención (`seleccionar_fecha_hora.html`), programa citas (`seleccionar_servicio.html`) y realiza seguimiento al estado de sus solicitudes.
* **🔧 Técnico:** Consulta el historial de atenciones asignadas, gestiona las órdenes de trabajo e ingresa diagnósticos y actualizaciones en tiempo real.
* **🛡️ Administrador:** Control total de usuarios, asignación de personal técnico, gestión de agendas y supervisión general de los servicios reportados.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python / Django (Patrón MVT)
* **Frontend:** HTML5, CSS3, JavaScript (Django Templates)
* **Base de Datos:** SQLite / PostgreSQL / MySQL
* **Control de Versiones:** Git & GitHub

---

## 🚀 Instalación y Configuración Local

Sigue esta guía paso a paso para configurar y ejecutar el proyecto en tu máquina local usando PostgreSQL:

### 1. Clonar el repositorio
```bash
git clone https://github.com/chaustrexp/Servitech-app.git
cd Servitech-app
```

### 2. Crear y activar el entorno virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

* **En Windows (PowerShell - Recomendado en VS Code):**
  ```powershell
  python -m venv venv
  venv\Scripts\Activate.ps1
  ```
  *(Si te da un error de políticas de ejecución en PowerShell, puedes ejecutar `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` en tu consola o usar directamente `venv\Scripts\python manage.py <comando>` sin activar).*

* **En Windows (CMD - Símbolo del sistema):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

* **En macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar dependencias
Con el entorno virtual activado, instala todas las librerías requeridas:
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos (PostgreSQL) y variables de entorno
El proyecto utiliza un archivo `.env` para gestionar la conexión a la base de datos.

1. En la raíz del proyecto (donde está `manage.py`), copia el archivo `.env.example` y renómbralo como `.env`:
```bash
# En Windows:
copy .env.example .env

# En macOS/Linux:
cp .env.example .env
```
2. Abre el archivo `.env` recién creado y reemplaza `tu_contraseña_aqui` con tu contraseña de PostgreSQL:

```env
# ⚠️ IMPORTANTE: USE_POSTGRES=True es obligatorio para conectar con PostgreSQL.
# Sin esta variable, el proyecto usará SQLite y los usuarios de tu BD no aparecerán.
USE_POSTGRES=True
DB_NAME=servitech
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui   # <-- Cambia solo esto
DB_HOST=localhost
DB_PORT=5432
```
*(Asegúrate de haber creado previamente una base de datos llamada `servitech` en tu motor de PostgreSQL, o utiliza el nombre que prefieras y configúralo en `DB_NAME`).*

### 5. Aplicar migraciones a la base de datos
Este comando creará las tablas necesarias en tu base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear un superusuario (Recomendado)
Para poder ingresar al panel de administración del sistema y gestionar usuarios:
```bash
python manage.py createsuperuser
```

### 7. Levantar el servidor
Finalmente, inicia el servidor de desarrollo de Django:
```bash
python manage.py runserver
```
¡Listo! Ya puedes acceder a la aplicación abriendo tu navegador en `http://127.0.0.1:8000/`.

---

## 💡 Solución a Errores Comunes

### ❌ `ModuleNotFoundError: No module named 'dotenv'` en Windows
Este error ocurre cuando ejecutas `python manage.py` sin que el entorno virtual esté activo (o porque no se activó correctamente).
1. Asegúrate de haber instalado las dependencias con `pip install -r requirements.txt` dentro del entorno virtual.
2. Si usas **PowerShell** (la terminal por defecto en VS Code), recuerda que ejecutar `venv\Scripts\activate` no funciona. Debes usar:
   ```powershell
   venv\Scripts\Activate.ps1
   ```
3. Alternativamente, puedes forzar el uso del Python del entorno virtual sin activarlo ejecutando:
   ```powershell
   venv\Scripts\python manage.py runserver
   ```