
# Create your models here.
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import generate_id
from apibackendapp.models import (
    LabTest, LabTestPrescription, Appointment,
    Patient, LabTestReport, Billing, Staff
)

# Auto ID for LabTestPrescription
@receiver(pre_save, sender=LabTestPrescription)
def auto_id_labtest_prescription(sender, instance, **kwargs):
    if not instance.lab_test_prescription_id:
        instance.lab_test_prescription_id = generate_id(
            prefix="LTP",
            model=LabTestPrescription,
            field_name="lab_test_prescription_id"
        )

# Auto ID for LabTestReport
@receiver(pre_save, sender=LabTestReport)
def auto_id_labtest_report(sender, instance, **kwargs):
    if not instance.report_id:
        instance.report_id = generate_id(
            prefix="RPT",
            model=LabTestReport,
            field_name="report_id"
        )

# Auto ID for Billing
@receiver(pre_save, sender=Billing)
def auto_id_billing(sender, instance, **kwargs):
    if not instance.bill_id:
        instance.bill_id = generate_id(
            prefix="BIL",
            model=Billing,
            field_name="bill_id"
        )

@receiver(pre_save, sender=LabTest)
def auto_id_labtest(sender, instance, **kwargs):
    if not instance.lab_test_id:
        instance.lab_test_id = generate_id(
            prefix="LT",
            model=LabTest,
            field_name="lab_test_id"
        )