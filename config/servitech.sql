-- =========================================================
-- BASE DE DATOS PARA SISTEMA DE AGENDAMIENTO DE SERVITECH
-- PostgreSQL
-- =========================================================


-- =========================================================
-- 1. TABLA USUARIO
-- Guarda clientes, técnicos, recepcionistas y administradores
-- Historias: HU-01, HU-02, HU-03, HU-04, HU-05, HU-06, HU-07, HU-08
-- =========================================================

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    contrasena VARCHAR(255) NOT NULL,

    rol VARCHAR(30) NOT NULL
        CHECK (rol IN (
            'CLIENTE',
            'TECNICO',
            'RECEPCIONISTA',
            'ADMINISTRADOR'
        )),

    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 2. TABLA ESPECIALIDAD
-- Guarda las especialidades que puede requerir un servicio
-- Historias: HU-01, HU-02 y HU-08
-- =========================================================

CREATE TABLE especialidad (
    id_especialidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- 3. TABLA SERVICIO
-- Catálogo de servicios del taller
-- Incluye dispositivo, duración, buffer y especialidad
-- Historias: HU-01 y HU-08
-- =========================================================

CREATE TABLE servicio (
    id_servicio SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL UNIQUE,

    descripcion VARCHAR(255),

    tipo_dispositivo VARCHAR(30) NOT NULL
        CHECK (tipo_dispositivo IN (
            'CELULAR',
            'LAPTOP',
            'PC'
        )),

    duracion_minutos INTEGER NOT NULL
        CHECK (duracion_minutos > 0),

    buffer_minutos INTEGER DEFAULT 0
        CHECK (buffer_minutos >= 0),

    id_especialidad INTEGER NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_servicio_especialidad
        FOREIGN KEY (id_especialidad)
        REFERENCES especialidad(id_especialidad)
);


-- =========================================================
-- 4. TABLA ESTADO_CITA
-- Estados posibles de una cita
-- Historias: HU-03, HU-04, HU-06 y HU-07
-- =========================================================

CREATE TABLE estado_cita (
    id_estado SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);


-- =========================================================
-- 5. TABLA HORARIO_TECNICO
-- Guarda los horarios de trabajo de cada técnico
-- Historia: HU-02
-- =========================================================

CREATE TABLE horario_tecnico (
    id_horario SERIAL PRIMARY KEY,

    id_tecnico INTEGER NOT NULL,

    dia_semana INTEGER NOT NULL
        CHECK (dia_semana BETWEEN 1 AND 7),

    hora_inicio TIME NOT NULL,

    hora_fin TIME NOT NULL,

    CONSTRAINT fk_horario_tecnico
        FOREIGN KEY (id_tecnico)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT chk_horario_valido
        CHECK (hora_fin > hora_inicio)
);


-- =========================================================
-- 6. TABLA CITA
-- Tabla principal del sistema
-- Historias: HU-01, HU-02, HU-03, HU-04, HU-05, HU-06 y HU-07
-- =========================================================

CREATE TABLE cita (
    id_cita SERIAL PRIMARY KEY,

    id_cliente INTEGER NOT NULL,

    id_tecnico INTEGER,

    id_servicio INTEGER NOT NULL,

    id_estado INTEGER NOT NULL DEFAULT 1,

    fecha DATE NOT NULL,

    hora_inicio TIME NOT NULL,

    hora_fin TIME NOT NULL,

    -- Datos relacionados con retrasos
    minutos_retraso INTEGER DEFAULT 0
        CHECK (minutos_retraso >= 0),

    -- Datos relacionados con cancelaciones
    motivo_cancelacion VARCHAR(255),

    -- Datos relacionados con reagendamientos
    motivo_reagendamiento VARCHAR(255),

    -- Datos relacionados con reparaciones extendidas
    minutos_adicionales INTEGER DEFAULT 0
        CHECK (minutos_adicionales >= 0),

    motivo_ajuste VARCHAR(255),

    observaciones VARCHAR(500),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    -- Relación con el cliente
    CONSTRAINT fk_cita_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES usuario(id_usuario),


    -- Relación con el técnico
    CONSTRAINT fk_cita_tecnico
        FOREIGN KEY (id_tecnico)
        REFERENCES usuario(id_usuario),


    -- Relación con el servicio
    CONSTRAINT fk_cita_servicio
        FOREIGN KEY (id_servicio)
        REFERENCES servicio(id_servicio),


    -- Relación con el estado
    CONSTRAINT fk_cita_estado
        FOREIGN KEY (id_estado)
        REFERENCES estado_cita(id_estado),


    -- Validar que la hora final sea mayor que la inicial
    CONSTRAINT chk_hora_cita
        CHECK (hora_fin > hora_inicio)
);


-- =========================================================
-- 7. TABLA HISTORIAL_CITA
-- Guarda los cambios de estado y acciones realizadas
-- Historias: HU-03, HU-04, HU-05, HU-06 y HU-07
-- =========================================================

CREATE TABLE historial_cita (
    id_historial SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    id_usuario INTEGER,

    estado_anterior VARCHAR(50),

    estado_nuevo VARCHAR(50),

    descripcion VARCHAR(255),

    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_historial_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE,


    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);


-- =========================================================
-- 8. TABLA NOTIFICACION
-- Guarda las notificaciones enviadas a los usuarios
-- Historias: HU-03, HU-04 y HU-05
-- =========================================================

CREATE TABLE notificacion (
    id_notificacion SERIAL PRIMARY KEY,

    id_usuario INTEGER,

    id_cita INTEGER NOT NULL,

    tipo VARCHAR(50) NOT NULL,

    mensaje VARCHAR(500) NOT NULL,

    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    leida BOOLEAN DEFAULT FALSE,


    CONSTRAINT fk_notificacion_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),


    CONSTRAINT fk_notificacion_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- DATOS INICIALES
-- =========================================================


-- =========================================================
-- INSERTAR ESTADOS DE LAS CITAS
-- =========================================================

INSERT INTO estado_cita (nombre, descripcion)
VALUES
('PENDIENTE', 'La cita fue creada pero aún no ha sido confirmada'),
('CONFIRMADA', 'La cita está confirmada'),
('RETRASADA', 'El cliente informó que llegará tarde'),
('EN_DIAGNOSTICO', 'El técnico está realizando el diagnóstico'),
('EN_REPARACION', 'El dispositivo se encuentra en reparación'),
('FINALIZADA', 'La atención de la cita terminó'),
('CANCELADA', 'La cita fue cancelada'),
('NO_SHOW', 'El cliente no asistió a la cita'),
('REAGENDADA', 'La cita fue cambiada para otra fecha u hora');


-- =========================================================
-- INSERTAR ESPECIALIDADES
-- =========================================================

INSERT INTO especialidad (nombre, descripcion)
VALUES
('CELULARES', 'Diagnóstico y reparación de dispositivos celulares'),
('LAPTOPS', 'Diagnóstico y reparación de computadores portátiles'),
('PC', 'Diagnóstico y reparación de computadores de escritorio'),
('SOFTWARE', 'Instalación y configuración de software'),
('HARDWARE', 'Reparación y mantenimiento de componentes físicos');


-- =========================================================
-- INSERTAR SERVICIOS
-- =========================================================

INSERT INTO servicio (
    nombre,
    descripcion,
    tipo_dispositivo,
    duracion_minutos,
    buffer_minutos,
    id_especialidad
)
VALUES
(
    'Diagnóstico de Celular',
    'Revisión general del dispositivo celular',
    'CELULAR',
    30,
    10,
    1
),
(
    'Diagnóstico de Laptop',
    'Revisión general del computador portátil',
    'LAPTOP',
    45,
    10,
    2
),
(
    'Diagnóstico de PC',
    'Revisión general del computador de escritorio',
    'PC',
    45,
    10,
    3
),
(
    'Reparación Exprés de Celular',
    'Reparación rápida de un dispositivo celular',
    'CELULAR',
    60,
    15,
    1
),
(
    'Asesoría de Software',
    'Asesoría para instalación y configuración de software',
    'PC',
    30,
    5,
    4
),
(
    'Mantenimiento de Hardware',
    'Mantenimiento preventivo de componentes físicos',
    'PC',
    60,
    15,
    5
);


-- =========================================================
-- FIN DEL SCRIPT
-- =========================================================4
CREATE OR REPLACE FUNCTION registrar_cambio_estado_cita()
RETURNS TRIGGER
AS $$
BEGIN

    -- Verificar si el estado de la cita cambió
    IF OLD.id_estado IS DISTINCT FROM NEW.id_estado THEN

        -- Registrar el cambio en el historial
        INSERT INTO historial_cita (
            id_cita,
            estado_anterior,
            estado_nuevo,
            descripcion,
            fecha_cambio
        )
        VALUES (
            NEW.id_cita,
            OLD.id_estado::VARCHAR,
            NEW.id_estado::VARCHAR,
            'Cambio de estado de la cita',
            CURRENT_TIMESTAMP
        );

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


-- =========================================================
-- CREAR TRIGGER
-- =========================================================

CREATE TRIGGER trigger_cambio_estado_cita
AFTER UPDATE OF id_estado
ON cita
FOR EACH ROW
EXECUTE FUNCTION registrar_cambio_estado_cita();