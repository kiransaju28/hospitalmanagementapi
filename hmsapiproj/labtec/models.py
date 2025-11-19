from django.db import models

class LabTestCategory(models.Model):
    # From tbllab_test_category
    category_name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.category_name

class LabTestParameter(models.Model):
    # From tbllab_test_parameter
    category = models.ForeignKey(
        LabTestCategory, 
        on_delete=models.CASCADE, 
        related_name="parameters"
    )
    parameter_key = models.CharField(max_length=10)
    label = models.CharField(max_length=20)
    normal_range = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category.category_name} - {self.label}"

class LabReport(models.Model):
    # From tblLab_Report
    appointment = models.ForeignKey(
        'reception.Appointment', 
        on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
        'reception.Patient', 
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        LabTestCategory, 
        on_delete=models.PROTECT 
    )
    report_date = models.DateField(auto_now_add=True)
    remarks = models.CharField(max_length=30, null=True, blank=True)
    sample_collected = models.BooleanField(default=False)
    
    # --- FIELD REMOVED ---
    # bill_amount = models.DecimalField(max_digits=10, decimal_places=2) - REMOVED

    def __str__(self):
        return f"Lab Report for {self.patient.patient_name} ({self.category.category_name})"

class LabReportResult(models.Model):
    # From tbllab_report_result
    lab_report = models.ForeignKey(
        LabReport, 
        on_delete=models.CASCADE, 
        related_name="results"
    )
    parameter = models.ForeignKey(
        LabTestParameter, 
        on_delete=models.PROTECT
    )
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.lab_report.id} - {self.parameter.label}: {self.value}"

# --- NEW MODELS ADDED ---
class LabBill(models.Model):
    """
    The "Header" for a lab bill. It is linked to the appointment
    and can contain multiple lab test items.
    """
    appointment = models.ForeignKey('reception.Appointment', on_delete=models.CASCADE)
    patient = models.ForeignKey('reception.Patient', on_delete=models.CASCADE)
    bill_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Lab Bill for {self.patient.patient_name} (Appt: {self.appointment.id})"

class LabBillItem(models.Model):
    """
    A single "Line Item" on a lab bill.
    Links one bill to one specific lab test.
    """
    bill = models.ForeignKey(LabBill, on_delete=models.CASCADE, related_name="items")
    test = models.ForeignKey(LabTestCategory, on_delete=models.PROTECT) # The test being billed
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of billing

    def __str__(self):
        return f"{self.test.category_name} for Bill {self.bill.id}"