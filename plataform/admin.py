from django.contrib import admin
from .models import Patient, DataPatient, Snack, Option


admin.site.register(Patient)
admin.site.register(DataPatient)
admin.site.register(Snack)
admin.site.register(Option)
