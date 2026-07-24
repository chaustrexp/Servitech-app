-- =========================================================
-- BASE DE DATOS: SISTEMA DE AGENDAMIENTO DE TALLER
-- MOTOR: POSTGRESQL
-- =========================================================


-- =========================================================
-- 1. TABLA ROL
-- =========================================================

CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL UNIQUE,

    descripcion VARCHAR(255),

    activo BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- 2. TABLA USUARIO
-- =========================================================

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,

    nombre_completo VARCHAR(150) NOT NULL,

    correo VARCHAR(150) UNIQUE NOT NULL,

    telefono VARCHAR(20),

    contrasena VARCHAR(255) NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 3. RELACIÓN USUARIO - ROL
-- =========================================================

CREATE TABLE usuario_rol (
    id_usuario INTEGER NOT NULL,

    id_rol INTEGER NOT NULL,

    PRIMARY KEY (id_usuario, id_rol),

    CONSTRAINT fk_usuario_rol_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT fk_usuario_rol_rol
        FOREIGN KEY (id_rol)
        REFERENCES rol(id_rol)
        ON DELETE CASCADE
);


-- =========================================================
-- 4. TABLA ESPECIALIDAD
-- =========================================================

CREATE TABLE especialidad (
    id_especialidad SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL UNIQUE,

    descripcion VARCHAR(255),

    activo BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- 5. TABLA TIPO DE DISPOSITIVO
-- =========================================================

CREATE TABLE tipo_dispositivo (
    id_tipo_dispositivo SERIAL PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL UNIQUE,

    activo BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- 6. TABLA ESTADO DE CITA
-- =========================================================

CREATE TABLE estado_cita (
    id_estado SERIAL PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL UNIQUE,

    descripcion VARCHAR(255),

    activo BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- 7. RELACIÓN TÉCNICO - ESPECIALIDAD
-- =========================================================

CREATE TABLE tecnico_especialidad (
    id_tecnico INTEGER NOT NULL,

    id_especialidad INTEGER NOT NULL,

    PRIMARY KEY (id_tecnico, id_especialidad),

    CONSTRAINT fk_tecnico_especialidad_tecnico
        FOREIGN KEY (id_tecnico)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT fk_tecnico_especialidad_especialidad
        FOREIGN KEY (id_especialidad)
        REFERENCES especialidad(id_especialidad)
        ON DELETE CASCADE
);


-- =========================================================
-- 8. TABLA SERVICIO
-- =========================================================

CREATE TABLE servicio (
    id_servicio SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL UNIQUE,

    descripcion VARCHAR(255),

    duracion_minutos INTEGER NOT NULL
        CHECK (duracion_minutos > 0),

    buffer_minutos INTEGER NOT NULL DEFAULT 0
        CHECK (buffer_minutos >= 0),

    id_especialidad INTEGER NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_servicio_especialidad
        FOREIGN KEY (id_especialidad)
        REFERENCES especialidad(id_especialidad)
);


-- =========================================================
-- 9. TABLA HORARIO DEL TÉCNICO
-- =========================================================

CREATE TABLE horario_tecnico (
    id_horario SERIAL PRIMARY KEY,

    id_tecnico INTEGER NOT NULL,

    dia_semana INTEGER NOT NULL
        CHECK (dia_semana BETWEEN 1 AND 7),

    hora_inicio TIME NOT NULL,

    hora_fin TIME NOT NULL,

    activo BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_horario_tecnico
        FOREIGN KEY (id_tecnico)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,

    CONSTRAINT chk_horario_valido
        CHECK (hora_fin > hora_inicio)
);


-- =========================================================
-- 10. TABLA CITA
-- =========================================================

CREATE TABLE cita (
    id_cita SERIAL PRIMARY KEY,

    id_cliente INTEGER NOT NULL,

    id_tecnico INTEGER,

    id_servicio INTEGER NOT NULL,

    id_tipo_dispositivo INTEGER NOT NULL,

    id_estado INTEGER NOT NULL DEFAULT 1,

    fecha DATE NOT NULL,

    hora_inicio TIME NOT NULL,

    hora_fin TIME NOT NULL,

    observaciones VARCHAR(500),

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cita_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES usuario(id_usuario),

    CONSTRAINT fk_cita_tecnico
        FOREIGN KEY (id_tecnico)
        REFERENCES usuario(id_usuario),

    CONSTRAINT fk_cita_servicio
        FOREIGN KEY (id_servicio)
        REFERENCES servicio(id_servicio),

    CONSTRAINT fk_cita_dispositivo
        FOREIGN KEY (id_tipo_dispositivo)
        REFERENCES tipo_dispositivo(id_tipo_dispositivo),

    CONSTRAINT fk_cita_estado
        FOREIGN KEY (id_estado)
        REFERENCES estado_cita(id_estado),

    CONSTRAINT chk_hora_cita
        CHECK (hora_fin > hora_inicio)
);


-- =========================================================
-- 11. HISTORIAL DE ESTADOS
-- =========================================================

CREATE TABLE historial_estado_cita (
    id_historial SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    id_estado_anterior INTEGER,

    id_estado_nuevo INTEGER NOT NULL,

    id_usuario INTEGER,

    motivo VARCHAR(255),

    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_historial_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE,

    CONSTRAINT fk_historial_estado_anterior
        FOREIGN KEY (id_estado_anterior)
        REFERENCES estado_cita(id_estado),

    CONSTRAINT fk_historial_estado_nuevo
        FOREIGN KEY (id_estado_nuevo)
        REFERENCES estado_cita(id_estado),

    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);


-- =========================================================
-- 12. TABLA RETRASO
-- =========================================================

CREATE TABLE retraso (
    id_retraso SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    minutos_retraso INTEGER NOT NULL
        CHECK (minutos_retraso > 0),

    fecha_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_retraso_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- 13. TABLA CANCELACIÓN
-- =========================================================

CREATE TABLE cancelacion (
    id_cancelacion SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    motivo VARCHAR(255) NOT NULL,

    fecha_cancelacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cancelacion_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- 14. TABLA REAGENDAMIENTO
-- =========================================================

CREATE TABLE reagendamiento (
    id_reagendamiento SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    fecha_anterior DATE NOT NULL,

    hora_anterior TIME NOT NULL,

    nueva_fecha DATE NOT NULL,

    nueva_hora TIME NOT NULL,

    motivo VARCHAR(255),

    fecha_reagendamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reagendamiento_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- 15. TABLA AJUSTE DE AGENDA
-- =========================================================

CREATE TABLE ajuste_agenda (
    id_ajuste SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    minutos_adicionales INTEGER NOT NULL
        CHECK (minutos_adicionales > 0),

    motivo VARCHAR(255) NOT NULL,

    fecha_ajuste TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ajuste_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- 16. TABLA NOTIFICACIÓN
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
-- 17. TABLA ENLACE SEGURO
-- =========================================================

CREATE TABLE enlace_seguro (
    id_enlace SERIAL PRIMARY KEY,

    id_cita INTEGER NOT NULL,

    token VARCHAR(255) UNIQUE NOT NULL,

    tipo_accion VARCHAR(50) NOT NULL,

    fecha_expiracion TIMESTAMP NOT NULL,

    utilizado BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_enlace_cita
        FOREIGN KEY (id_cita)
        REFERENCES cita(id_cita)
        ON DELETE CASCADE
);


-- =========================================================
-- INSERTAR ROLES
-- =========================================================

INSERT INTO rol (nombre, descripcion)
VALUES
    ('CLIENTE', 'Cliente que agenda y administra sus citas'),

    ('TECNICO', 'Técnico encargado de atender las citas'),

    ('RECEPCIONISTA', 'Usuario encargado de gestionar la recepción'),

    ('ADMINISTRADOR', 'Usuario encargado de administrar el sistema');


-- =========================================================
-- INSERTAR TIPOS DE DISPOSITIVOS
-- =========================================================

INSERT INTO tipo_dispositivo (nombre)
VALUES
    ('Celular'),
    ('Laptop'),
    ('PC');


-- =========================================================
-- INSERTAR ESTADOS DE CITA
-- =========================================================

INSERT INTO estado_cita (nombre, descripcion)
VALUES
    ('PENDIENTE', 'La cita fue creada pero aún no ha sido confirmada'),

    ('CONFIRMADA', 'La cita está confirmada'),

    ('RETRASADA', 'El cliente informó que llegará tarde'),

    ('EN_DIAGNOSTICO', 'El técnico está realizando el diagnóstico'),

    ('EN_REPARACION', 'El equipo está siendo reparado'),

    ('FINALIZADA', 'La atención fue completada'),

    ('CANCELADA', 'La cita fue cancelada'),

    ('NO_SHOW', 'El cliente no asistió'),

    ('REAGENDADA', 'La cita fue movida a otra fecha');


-- =========================================================
-- INSERTAR ESPECIALIDADES
-- =========================================================

INSERT INTO especialidad
(nombre, descripcion)
VALUES
    ('Diagnóstico',
     'Diagnóstico general de dispositivos'),

    ('Hardware',
     'Reparación y mantenimiento de componentes físicos'),

    ('Software',
     'Instalación, configuración y reparación de software'),

    ('Celulares',
     'Reparación y mantenimiento de teléfonos celulares'),

    ('Computadores',
     'Reparación y mantenimiento de computadores y laptops');