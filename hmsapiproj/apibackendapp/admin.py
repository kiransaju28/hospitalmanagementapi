from django.contrib import admin
from .models import (
    Staff, Specialization, Doctor, 
    Patient, Appointment, MedicineCategory, Medicine,
    MedicinePrescription, Consultation, MedicineStock,
    LabTest, LabTestPrescription, Billing, LabTestReport
)

from apibackendapp.models import (
    LabTest, LabTestPrescription, LabTestReport)
# Register your models here.
