

# Register your models here.
from django.contrib import admin
from apibackendapp.models import (
    LabTest, LabTestPrescription, LabTestReport
)

admin.site.register(LabTest)
admin.site.register(LabTestPrescription)
admin.site.register(LabTestReport)
