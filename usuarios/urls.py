from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_view, name='login'),
    path('registro/', views.auth_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]