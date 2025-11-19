from django.contrib import admin
from .models import Patient, Appointment,ConsultationBill

# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(ConsultationBill)