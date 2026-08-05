from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        extra_fields.setdefault('username', correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.Rol.ADMINISTRADOR)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)

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
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        verbose_name='Foto de Perfil'
    )

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_completo']

    objects = UsuarioManager()

    @property
    def es_admin(self):
        return self.rol in [self.Rol.ADMINISTRADOR, 'ADMIN']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.correo
        if self.rol == 'ADMIN':
            self.rol = self.Rol.ADMINISTRADOR
        self.is_active = self.activo
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_completo} ({self.correo}) - {self.rol}"
