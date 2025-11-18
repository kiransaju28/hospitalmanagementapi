from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import generate_id

# Note: We are creating a custom user model 'SystemUser' to match your 'tblUser' table.
# In a standard new Django project, we would usually use django.contrib.auth.models.User.

class Role(models.Model):
    role_id = models.CharField(max_length=10, primary_key=True)
    role_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tblrole'

    def __str__(self):
        return self.role_name

class SystemUser(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'tblUser'

    def __str__(self):
        return self.username

class Staff(models.Model):
    staff_id = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    mail_id = models.CharField(max_length=30, null=True, blank=True)
    mobileno = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblstaff'

    def __str__(self):
        return self.fullname

class Specialization(models.Model):
    specialization_id = models.CharField(max_length=10, primary_key=True)
    specialization_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tblspecialization'

    def __str__(self):
        return self.specialization_name

class Doctor(models.Model):
    doctor_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    contact_info = models.IntegerField(null=True, blank=True) # SQL said INT
    consultation_fee = models.IntegerField(null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbldoctor'

    def __str__(self):
        return self.name if self.name else self.doctor_id

class Patient(models.Model):
    patient_id = models.CharField(max_length=10, primary_key=True)
    patient_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    contact_info = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'tblpatient'

    def __str__(self):
        return self.patient_name

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=20, primary_key=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    token_number = models.IntegerField(null=True, blank=True)
    consultation_status = models.BooleanField(default=False) # SQL said bool
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblappointment'

    def __str__(self):
        return f"{self.appointment_id} - {self.patient.patient_name}"

class MedicineCategory(models.Model):
    medicine_category_id = models.CharField(max_length=10, primary_key=True)
    medicine_category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tblmedicinecategory'

    def __str__(self):
        return self.medicine_category_name

class Medicine(models.Model):
    medicine_id = models.CharField(max_length=10, primary_key=True)
    medicine_name = models.CharField(max_length=255)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    medicine_category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblmedicine'

    def __str__(self):
        return self.medicine_name

class MedicinePrescription(models.Model):
    medicine_prescription_id = models.CharField(max_length=10, primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.IntegerField(null=True, blank=True)
    frequency = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblmedicineprescription'

class Consultation(models.Model):
    consultation_id = models.CharField(max_length=10, primary_key=True)
    symptoms = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True) # Mapped to DEFAULT CURRENT_TIMESTAMP
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblconsultation'

class MedicineStock(models.Model):
    medicine_stock_id = models.CharField(max_length=10, primary_key=True)
    stock_in_hand = models.IntegerField(default=0)
    re_order_level = models.IntegerField(default=0)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblmedicinestock'

class LabTest(models.Model):
    lab_test_id = models.CharField(max_length=10, primary_key=True, blank=True)
    lab_test_name = models.CharField(max_length=255)
    amount = models.IntegerField(null=True, blank=True)
    min_range = models.IntegerField(null=True, blank=True)
    max_range = models.IntegerField(null=True, blank=True)
    sample_collected = models.BooleanField(default=True)

    class Meta:
        db_table = 'tblLabtest'
    
    def __str__(self):
        return self.lab_test_name


@receiver(pre_save, sender=LabTest)
def auto_id_labtest(sender, instance, **kwargs):
    if not instance.lab_test_id:
        instance.lab_test_id = generate_id(
            prefix="LT",
            model=LabTest,
            field_name="lab_test_id"
        )


class LabTestPrescription(models.Model):
    lab_test_prescription_id = models.CharField(max_length=10, primary_key=True)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    lab_test_value = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblLabtestprescription'

class Billing(models.Model):
    bill_id = models.CharField(max_length=10, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill_date = models.DateField(null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'tblbilling'

class LabTestReport(models.Model):
    report_id = models.CharField(max_length=10, primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE) # Unique in SQL means OneToOne in Django
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    overall_remarks = models.TextField(null=True, blank=True)
    report_status = models.CharField(max_length=20, default='Pending')

    class Meta:
        db_table = 'tblLabtestreport'