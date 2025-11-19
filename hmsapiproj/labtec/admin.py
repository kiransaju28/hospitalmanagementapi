from django.contrib import admin
from .models import LabTestCategory, LabTestParameter, LabReport, LabReportResult,LabBill,LabBillItem

# Register your models here.
admin.site.register(LabTestCategory)
admin.site.register(LabTestParameter)
admin.site.register(LabReport)
admin.site.register(LabReportResult)
admin.site.register(LabBill)
admin.site.register(LabBillItem)