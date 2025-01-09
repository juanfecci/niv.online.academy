from django.urls import path
from . import views

app_name = 'diagnostico'

urlpatterns = [
    path('', views.prueba_diagnostico, name='prueba_diagnostico'),
    path('test/', views.prueba_diagnostico2, name='prueba_diagnostico2'),
]
