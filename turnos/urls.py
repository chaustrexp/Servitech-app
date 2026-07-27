# Las rutas de las páginas


from django.urls import path
from . import views

urlpatterns = [
    path('servicios/dispositivo/', views.seleccionar_dispositivo, name='seleccionar_dispositivo'),
]