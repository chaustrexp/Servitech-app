# Las tablas SQL que definimos

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# 0. MANAGER DE USUARIOS PERSONALIZADO
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        """Crea y guarda un usuario con el correo y contraseña dados."""
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        extra_fields.setdefault('username', correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """Crea y guarda un superusuario con el correo y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.Rol.ADMINISTRADOR)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)


# 1. USUARIO (Hereda de AbstractUser)
class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        TECNICO = 'TECNICO', 'Técnico'
        RECEPCIONISTA = 'RECEPCIONISTA', 'Recepcionista'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'

    id_usuario = models.BigAutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    correo = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(
        max_length=30,
        choices=Rol.choices,
        default=Rol.CLIENTE
    )
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Autenticación usando Correo Electrónico
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_completo']

    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.correo
        self.is_active = self.activo
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_completo} ({self.correo}) - {self.rol}"


# 2. ESPECIALIDAD
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# 3. SERVICIO
class Servicio(models.Model):
    TIPO_DISPOSITIVO_CHOICES = [
        ('CELULAR', 'Celular'),
        ('LAPTOP', 'Laptop'),
        ('PC', 'PC'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    tipo_dispositivo = models.CharField(max_length=30, choices=TIPO_DISPOSITIVO_CHOICES)
    duracion_minutos = models.IntegerField()
    buffer_minutos = models.IntegerField(default=0)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='servicios')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_dispositivo})"


# 4. ESTADO CITA
class EstadoCita(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre


# 5. HORARIO TÉCNICO
class HorarioTecnico(models.Model):
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField() # 1 a 7
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Día {self.dia_semana}: {self.hora_inicio} - {self.hora_fin}"


# 6. CITA / TURNO (Tabla Principal)
class Cita(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas_cliente')
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_tecnico')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoCita, on_delete=models.PROTECT, null=True, blank=True)
    
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    # Contingencias y Retrasos
    minutos_retraso = models.IntegerField(default=0)
    motivo_cancelacion = models.CharField(max_length=255, blank=True, null=True)
    motivo_reagendamiento = models.CharField(max_length=255, blank=True, null=True)
    minutos_adicionales = models.IntegerField(default=0)
    motivo_ajuste = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita #{self.id} - {self.cliente.correo} ({self.fecha})"


# 7. HISTORIAL CITA
class HistorialCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=50, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)


# 8. NOTIFICACIÓN
class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=500)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)