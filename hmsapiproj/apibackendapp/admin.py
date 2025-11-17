from django.contrib import admin
from .models import (
    Staff, Specialization, Doctor, 
    Patient, Appointment, MedicineCategory, Medicine,
    MedicinePrescription, Consultation, MedicineStock,
    LabTest, LabTestPrescription, Billing, LabTestReport
)

# Register your models here.
admin.site.register(Staff)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicineCategory)
admin.site.register(Medicine)
admin.site.register(MedicinePrescription)
admin.site.register(Consultation)
admin.site.register(MedicineStock)
admin.site.register(LabTest)
admin.site.register(LabTestPrescription)
admin.site.register(Billing)
admin.site.register(LabTestReport)