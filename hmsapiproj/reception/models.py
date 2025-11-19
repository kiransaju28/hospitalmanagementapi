from django.db import models

class Patient(models.Model):
    # From tblpatient
    patient_name = models.CharField(max_length=40)
    age = models.IntegerField()
    email = models.EmailField(max_length=40, unique=True, null=True, blank=True)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.patient_name} (ID: {self.id})"

class Appointment(models.Model):
    # From tblappointment
    token = models.CharField(max_length=20)
    appointment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Scheduled') # e.g., Scheduled, Completed
    
    # Link to a model in *this* app (Patient)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    # Link to a model in *another* app (admins.Doctor)
    doctor = models.ForeignKey(
        'admins.Doctor', 
        on_delete=models.SET_NULL, 
        null=True
    )

    def __str__(self):
        return f"Appointment for {self.patient.patient_name} on {self.appointment_date.date()}"

# --- NEW MODEL ADDED ---
class ConsultationBill(models.Model):
    """
    Stores the bill for a single consultation.
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Stores the doctor's fee

    def __str__(self):
        return f"Consult Bill for {self.patient.patient_name} (Appt: {self.appointment.id})"