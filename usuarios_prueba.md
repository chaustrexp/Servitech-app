# Datos de Prueba - Plataforma Servitech

La base de datos ha sido restablecida y se han inyectado datos iniciales para poder probar todos los flujos de la plataforma. A continuación, te presento las credenciales para acceder con los distintos roles y la estructura generada.

## Credenciales de Acceso

| Nombre | Rol | Correo / Usuario | Contraseña |
|---|---|---|---|
| Administrador Principal | `ADMINISTRADOR` | `admin@servitech.com` | `admin123` |
| Tecnico Celulares | `TECNICO` | `tec.cel@servitech.com` | `tecnico123` |
| Tecnico Laptops | `TECNICO` | `tec.lap@servitech.com` | `tecnico123` |
| Tecnico General | `TECNICO` | `tec.gen@servitech.com` | `tecnico123` |
| Ana Torres | `CLIENTE` | `ana.torres@gmail.com` | `cliente123` |
| Carlos Mendoza | `CLIENTE` | `carlos.mendoza@gmail.com` | `cliente123` |
| María García | `CLIENTE` | `maria.garcia@gmail.com` | `cliente123` |
| Roberto López | `CLIENTE` | `roberto.lopez@gmail.com` | `cliente123` |

> [!TIP]
> Recuerda que el sistema pide el **correo electrónico** para iniciar sesión, no el nombre de la persona.

## Estructura Generada

### Especialidades
- **GENERAL**: General
- **CELULARES**: Móviles y Tablets
- **LAPTOPS**: Computadores Portátiles

### Servicios Base
1. Reparación de Pantalla Laptop (90 min)
2. Cambio de Pantalla OLED (60 min)
3. Diagnóstico de Rendimiento (60 min)
4. Cambio de Batería y Mantenimiento (45 min)

### Citas Generadas (Automáticas)
Se han asignado citas en diferentes estados para que los paneles de administración y el dashboard de técnicos cuenten con datos reales:
- 1 Cita **PENDIENTE** para hoy.
- 1 Cita **CONFIRMADA** para hoy.
- 1 Cita **EN DIAGNÓSTICO** para hoy.
- 1 Cita **FINALIZADA** del día de ayer.
