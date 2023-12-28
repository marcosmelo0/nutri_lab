from django.contrib import admin
from .models import Patient, DataPatient


admin.site.register(Patient)
admin.site.register(DataPatient)
