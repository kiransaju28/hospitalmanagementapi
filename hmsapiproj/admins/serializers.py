from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Staff, Doctor, Department
from reception.models import ConsultationBill
from labtec.models import LabBill
from pharmacist.models import pharmacistBill

# --- Import the Doctor's History Serializer ---
from doctor.serializers import PatientHistorySerializer

ROLE_CHOICES = (
    ('Doctor', 'Doctor'),
    ('reception', 'reception'),
    ('labtec', 'labtec'),
    ('Pharmacist', 'Pharmacist'),
)

class UserRegistrationSerializer(serializers.Serializer):
    """
    Special serializer to create a new User, Staff, 
    and (if needed) Doctor, all at once.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    
    # Staff fields
    full_name = serializers.CharField()
    gender = serializers.CharField()
    joining_date = serializers.DateField()
    mobile_number = serializers.CharField()
    
    # Doctor fields (optional)
    consultation_fee = serializers.IntegerField(required=False, allow_null=True)
    designation = serializers.CharField(required=False, allow_null=True, max_length=20)
    availability = serializers.CharField(required=False, allow_null=True, max_length=30)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        required=False, 
        allow_null=True
    )

    def validate(self, data):
        if data['role'] == 'Doctor':
            if (not data.get('consultation_fee') or 
                not data.get('designation') or 
                not data.get('department') or
                not data.get('availability')):
                raise serializers.ValidationError(
                    "Doctor role requires consultation_fee, designation, availability, and department."
                )
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        role_name = validated_data['role']
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)
        
        staff = Staff.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            gender=validated_data['gender'],
            joining_date=validated_data['joining_date'],
            mobile_number=validated_data['mobile_number']
        )
        
        if role_name == 'Doctor':
            Doctor.objects.create(
                staff=staff,
                consultation_fee=validated_data['consultation_fee'],
                designation=validated_data['designation'],
                department=validated_data['department'],
                availability=validated_data['availability']
            )
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class StaffSerializer(serializers.ModelSerializer): # <-- THIS IS THE CLASS YOUR ERROR WAS MISSING
    """ 
    Serializer for viewing and editing Staff details.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.groups.first.name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['id', 'full_name', 'gender', 'joining_date', 'mobile_number', 'username', 'role']
        read_only_fields = ['username', 'role']

class StaffDetailSerializer(serializers.ModelSerializer):
    """ Read-only view for Staff details """
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.groups.first.name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['id', 'full_name', 'username', 'role', 'mobile_number', 'joining_date']

class DoctorSerializer(serializers.ModelSerializer):
    """ 
    Serializer for viewing and editing Doctor details.
    """
    staff = StaffSerializer(read_only=True) 
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), 
        source='staff', 
        write_only=True
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        source='department', 
        write_only=True
    )
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 
            'staff', 
            'staff_id',
            'consultation_fee', 
            'designation', 
            'availability',
            'department', 
            'department_id' 
        ]

class DoctorDetailSerializer(serializers.ModelSerializer):
    """ Read-only view for Doctor details """
    staff = StaffDetailSerializer(read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'staff', 'consultation_fee', 'designation', 'availability', 'department_name']

# --- BILLING SERIALIZERS ---

class SimpleConsultationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = ['bill_date', 'amount']

class SimpleLabBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabBill
        fields = ['bill_date', 'total_amount']

# --- ADD THIS NEW CLASS ---
class SimplepharmacistBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = pharmacistBill
        fields = ['bill_date', 'total_amount']

# --- ADMIN/reception PATIENT HISTORY ---

class AdminPatientHistorySerializer(PatientHistorySerializer):
    """
    Inherits from Doctor's serializer but ADDS billing information.
    Used for Admin and reception.
    """
    consultation_bills = SimpleConsultationBillSerializer(many=True, read_only=True, source='consultationbill_set')
    lab_bills = SimpleLabBillSerializer(many=True, read_only=True, source='labbill_set')
    
    # --- ADD THIS LINE ---
    pharmacist_bills = SimplepharmacistBillSerializer(many=True, read_only=True, source='pharmacistbill_set')

    class Meta(PatientHistorySerializer.Meta):
        # --- UPDATE THIS LIST ---
        fields = PatientHistorySerializer.Meta.fields + ['consultation_bills', 'lab_bills', 'pharmacist_bills']