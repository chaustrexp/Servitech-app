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