from django.db import models

class BasicVitals(models.Model):
    # From tblbasic_vitals
    # Linked to an Appointment, not a Patient, since vitals are per-visit
    appointment = models.OneToOneField(
        'reception.Appointment', 
        on_delete=models.CASCADE
    )
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure = models.CharField(max_length=10, null=True, blank=True) # e.g., "120/80"
    blood_sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Vitals for Appointment {self.appointment.id}"

class Consultation(models.Model):
    # From tblconsultation
    # This is the main record for a doctor's visit
    appointment = models.OneToOneField(
        'reception.Appointment', 
        on_delete=models.CASCADE
    )
    vitals = models.OneToOneField(
        BasicVitals, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    symptoms = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # --- NEW FIELDS ADDED ---
    # These booleans track if the patient will use the hospital's
    # internal pharmacist and lab, or go outside.
    fulfill_pharmacist_internally = models.BooleanField(default=True)
    fulfill_lab_internally = models.BooleanField(default=True)
    # --------------------------

    def __str__(self):
        return f"Consultation for {self.appointment.patient.patient_name}"

class PrescriptionItem(models.Model):
    # From tblprescription
    # This is one *line item* on a prescription
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name="prescription_items" # Lets you get all items for a consultation
    )
    medicine = models.ForeignKey(
        'pharmacist.Medicine', 
        on_delete=models.PROTECT # Don't delete medicine if it's in a prescription
    )
    dosage = models.CharField(max_length=10) # e.g., "500mg"
    frequency = models.CharField(max_length=20) # e.g., "1-0-1"
    duration = models.CharField(max_length=10) # e.g., "5 days"

    def __str__(self):
        return f"{self.medicine.medicine_name} for {self.consultation.appointment.patient.patient_name}"

# --- NEW MODEL ADDED ---
class LabTestOrder(models.Model):
    """
    This links a Consultation to a Lab Test that the doctor ordered.
    It's just like PrescriptionItem, but for labs.
    """
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="lab_test_orders" # Lets you get all lab orders for a consultation
    )
    test = models.ForeignKey(
        'labtec.LabTestCategory', # Links to the test
        on_delete=models.PROTECT
    )
    # You could add an optional 'notes' field here if needed
    # notes = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.test.category_name} for {self.consultation.appointment.patient.patient_name}"