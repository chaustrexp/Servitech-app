# Las rutas de las páginas


from django.urls import path
from . import views

urlpatterns = [
    path('turno/<str:codigo_turno>/', views.ver_turno, name='ver_turno'),
    path('turno/<int:turno_id>/retraso/', views.notificar_retraso, name='notificar_retraso'),
]