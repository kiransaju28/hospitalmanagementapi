from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    # From tbldepartment
    department_name = models.CharField(max_length=30)

    def __str__(self):
        return self.department_name

class Staff(models.Model):
    # From tblstaff
    # This links your staff profile to a Django login User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=10, unique=True)
    
    # The 'role' (e.g., 'Doctor', 'reception') is handled 
    # by adding the User to a Django "Group", so role_id is not needed.

    def __str__(self):
        return self.full_name

class Doctor(models.Model):
    # From tbldoctor
    # This links the Doctor-specific details to a Staff profile
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    
    consultation_fee = models.IntegerField()
    designation = models.CharField(max_length=20)
    availability = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        # Access the full_name from the related Staff model
        return f"Dr. {self.staff.full_name}"