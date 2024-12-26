from django.urls import path
from . import views

urlpatterns = [
    path('', views.prueba_diagnostico, name='diagnostico'),
]
