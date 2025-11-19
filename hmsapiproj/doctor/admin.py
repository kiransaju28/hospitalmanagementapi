from django.contrib import admin
from .models import BasicVitals, Consultation, PrescriptionItem,LabTestOrder

# Register your models here.
admin.site.register(BasicVitals)
admin.site.register(Consultation)
admin.site.register(PrescriptionItem)
admin.site.register(LabTestOrder)