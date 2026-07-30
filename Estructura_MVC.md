MediQQTA/
├── agendamiento/                 # Tu aplicación principal
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py                  # Configuración del panel de administración
│   ├── urls.py                   # Enrutador (asigna URLs a los Controladores/Vistas)
│   │
│   ├── models/                   # 🗄️ MODELOS (La "M" en MVC)
│   │   ├── __init__.py           # <- Importas todos los modelos aquí
│   │   ├── usuarios.py           # Contiene: Usuario, Rol
│   │   ├── pacientes.py          # Contiene: Paciente, Entidad
│   │   ├── citas.py              # Contiene: Cita, BloqueoAgenda
│   │   └── configuracion.py      # Contiene: ConfiguracionSistema, LogAuditoria
│   │
│   ├── views/                    # 🎮 CONTROLADORES (La "C" en MVC)
│   │   ├── __init__.py           # <- Importas todas las vistas aquí
│   │   ├── auth_views.py         # Login, Logout
│   │   ├── dashboard_views.py    # Dashboard principal
│   │   ├── citas_views.py        # Agendar, listar, cancelar, reagendar citas
│   │   ├── pacientes_views.py    # Listar pacientes, crear pacientes
│   │   └── config_views.py       # Configuración del sistema, reportes
│   │
│   ├── services/                 # ⚙️ LÓGICA DE NEGOCIO (Patrón Service Layer)
│   │   ├── __init__.py
│   │   ├── citas_service.py      # Validaciones complejas: is_time_slot_available
│   │   └── reportes_service.py   # Generación de Excels y PDFs
│   │
│   └── templates/                # 🎨 VISTAS / INTERFAZ (La "V" en MVC)
│       └── agendamiento/
│           ├── login.html
│           ├── dashboard.html
│           └── ... (demás HTML)
