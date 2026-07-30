# 🛠️ ServiTech - Sistema de Agendamiento y Gestión de Turnos Digitales

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

ServiTech es una solución web integral diseñada para optimizar la gestión de citas, agendamiento de servicios técnicos de reparación y asignación de turnos digitales en tiempo real, minimizando los tiempos de espera e integrando mecanismos de contingencia ante retrasos.

---

## 🚀 Características Principales

* **📅 Agendamiento de Servicios (Flujo B2C):** Selección paso a paso de dispositivo, tipo de servicio y horario disponible en tiempo real.
* **🎫 Turno Digital Interactivo:** Generación de código único de turno (`T-014`) con badge de estado dinámico y tiempos estimados de espera.
* **⚠️ Gestión de Contingencias (RN-03):** Ventana restringida para que clientes autenticados notifiquen retrasos de máximo 10 minutos con anticipación.
* **💻 Dashboard del Técnico:** Panel para visualizar citas asignadas del día, filtrar por servicio y aplicar extensiones de tiempo (`+15 min`).
* **⚙️ Panel Administrativo (HU-08):** Supervisión global mediante KPIs operacionales y catálogo de servicios configurable (duración, especialidades y buffers de limpieza).

---

## 🏛️ Arquitectura y Tecnologías

* **Backend:** Python / Django (Patrón MVT)
* **Frontend:** Django Templates + Tailwind CSS (Diseño Responsive)
* **Base de Datos:** PostgreSQL / MySQL (Soporte local para SQLite3 en desarrollo)
* **Control de Versiones:** Git & GitHub

---

## 📋 Reglas de Negocio Destacadas (RN)

* **RN-01 (Tolerancia):** Margen máximo predeterminado para llegada sin aviso es de **15 minutos**.
* **RN-02 (Buffer entre Citas):** Margen automático de **5 a 10 minutos** entre turnos para limpieza y preparación de la mesa de trabajo del técnico.
* **RN-03 (Ventana de Retraso):** El cliente autenticado puede notificar un retraso de 10 min únicamente con al menos **10 minutos de anticipación**. Se permite un único aviso por turno.

---

## 📂 Estructura del Proyecto

```text
ServiTech/
├── manage.py
├── serviTech/                  # Configuración principal del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── turnos/                     # Aplicación principal del módulo de agendamiento
│   ├── models.py               # Modelos ORM (Usuarios, Turnos, Servicios, Dispositivos)
│   ├── views.py                # Lógica de negocio y renderizado de vistas
│   ├── urls.py                 # Enrutamiento de URLs
│   ├── admin.py                # Configuración del panel de administración
│   ├── static/                 # Estilos globales y scripts
│   └── templates/              # Interfaz HTML (Django Templates)
│       └── turnos/
│           ├── base.html
│           ├── agendamiento.html
│           ├── turno_digital.html
│           ├── dashboard_tecnico.html
│           └── admin_dashboard.html
└── README.md

---

## 🛠️ Instrucciones de Instalación (Para Desarrolladores)

Sigue estos pasos para clonar y ejecutar el proyecto en tu máquina local.

### 1. Clonar el repositorio
Abre tu terminal y ejecuta:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Servitech-app-main
```

### 2. Crear y activar un entorno virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias:
```bash
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
Con el entorno virtual activado, instala los paquetes necesarios:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos (PostgreSQL)
El proyecto utiliza PostgreSQL. Debes crear una base de datos local y configurar tus credenciales:

1. Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `manage.py`).
2. Copia el contenido del archivo `.env.example` dentro de tu nuevo `.env`:
   ```env
   DB_NAME=servitech
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña_aqui
   DB_HOST=localhost
   DB_PORT=5432
   ```
3. Reemplaza `tu_contraseña_aqui` por tu contraseña real de PostgreSQL.
4. Asegúrate de crear una base de datos vacía llamada `servitech` (o el nombre que hayas puesto en `DB_NAME`) en tu servidor local de PostgreSQL.

### 5. Aplicar Migraciones
Django creará las tablas necesarias en la base de datos automáticamente:
```bash
python manage.py migrate
```

### 6. Ejecutar el Servidor
Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```
Abre tu navegador y ve a `http://127.0.0.1:8000/`. ¡El proyecto debería estar funcionando!