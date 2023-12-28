from django.urls import path
from . import views


urlpatterns = [
    path('patients/', views.patient, name="patient"),
]
