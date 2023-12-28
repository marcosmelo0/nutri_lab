from django.urls import path
from . import views


urlpatterns = [
    path('patients/', views.patient, name="patient"),
    path('patient-data-list/', views.patient_data_list, name="patient_data_list"),
    path('patient-data/<str:id>/', views.patient_data, name="patient-data"),
]
