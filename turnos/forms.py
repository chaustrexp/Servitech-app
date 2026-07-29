from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario de registro público de usuarios.
    Asigna por defecto el rol CLIENTE y valida correo electrónico único.
    """
    nombre_completo = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
            'placeholder': 'Ej. Juan Pérez'
        }),
        label="Nombre Completo"
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
            'placeholder': 'correo@ejemplo.com'
        }),
        label="Correo Electrónico"
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
            'placeholder': '+57 300 123 4567'
        }),
        label="Teléfono (Opcional)"
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('nombre_completo', 'email', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de estilos Tailwind a los campos de contraseña heredados
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
                'placeholder': '••••••••'
            })
            self.fields['password1'].label = "Contraseña"
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
                'placeholder': '••••••••'
            })
            self.fields['password2'].label = "Confirmar Contraseña"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(correo__iexact=email).exists():
            raise ValidationError("Ya existe una cuenta asociada a este correo electrónico.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.correo = self.cleaned_data['email']
        usuario.username = self.cleaned_data['email']
        usuario.nombre_completo = self.cleaned_data['nombre_completo']
        usuario.telefono = self.cleaned_data.get('telefono', '')
        usuario.rol = Usuario.Rol.CLIENTE  # Rol asignado automáticamente por defecto

        if commit:
            usuario.save()
        return usuario


class CustomLoginForm(AuthenticationForm):
    """
    Formulario de autenticación para inicio de sesión utilizando Correo Electrónico.
    """
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none transition',
            'placeholder': '••••••••'
        })
    )
