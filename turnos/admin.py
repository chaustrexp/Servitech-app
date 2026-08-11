from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especialidad, Servicio, EstadoCita, HorarioTecnico, Cita, HistorialCita, Notificacion, Usuario, Repuesto, Inventario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin para gestionar usuarios y sus roles."""
    list_display = ('correo', 'nombre_completo', 'rol', 'activo', 'fecha_registro')
    list_filter = ('rol', 'activo')
    search_fields = ('correo', 'nombre_completo')
    ordering = ('-fecha_registro',)
    list_editable = ('rol', 'activo')

    fieldsets = (
        ('Información Personal', {'fields': ('correo', 'nombre_completo', 'telefono', 'password')}),
        ('Rol y Estado', {'fields': ('rol', 'activo')}),
        ('Permisos Django', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre_completo', 'telefono', 'rol', 'password1', 'password2'),
        }),
    )


admin.site.register(Especialidad)
admin.site.register(Servicio)
admin.site.register(EstadoCita)
admin.site.register(HorarioTecnico)
admin.site.register(Cita)
admin.site.register(HistorialCita)
admin.site.register(Notificacion)
admin.site.register(Repuesto)
admin.site.register(Inventario)

from .models.soporte import EstadoSistema, TicketSoporte

@admin.register(EstadoSistema)
class EstadoSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'ultima_actualizacion')
    list_filter = ('estado',)

@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'area', 'urgencia', 'estado', 'tecnico', 'fecha_creacion')
    list_filter = ('estado', 'urgencia', 'area')
    search_fields = ('titulo', 'descripcion')
