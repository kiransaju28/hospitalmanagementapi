from rest_framework import serializers
from apibackendapp.models import (
    MedicineCategory, Medicine, MedicineStock, 
    MedicinePrescription, Appointment, Patient # Need Appointment and Patient for nested data
)

# --- NESTED SERIALIZERS (Helper for detailed views) ---
# These small serializers help embed related object details without 'depth=1'.

class SimpleMedicineSerializer(serializers.ModelSerializer):
    """Used to embed medicine details inside a prescription or stock view."""
    class Meta:
        model = Medicine
        fields = ['medicine_id', 'medicine_name', 'price']

class SimplePatientSerializer(serializers.ModelSerializer):
    """Used to embed patient details inside an appointment view."""
    class Meta:
        model = Patient
        fields = ['patient_id', 'patient_name', 'contact_info']


# --- 1. MEDICINE CATEGORY SERIALIZERS ---

class MedicineCategorySerializer(serializers.ModelSerializer):
    """Standard serializer for CRUD operations on MedicineCategory."""
    class Meta:
        model = MedicineCategory
        fields = '__all__'


# --- 2. MEDICINE SERIALIZERS ---

class Medicine_ReadSerializer(serializers.ModelSerializer):
    """For GET requests: shows full category details."""
    medicine_category = MedicineCategorySerializer(read_only=True) # Nested object details
    
    class Meta:
        model = Medicine
        fields = '__all__'
        
class Medicine_WriteSerializer(serializers.ModelSerializer):
    """For POST/PUT requests: expects only the category ID."""
    medicine_category_id = serializers.CharField(
        source='medicine_category.medicine_category_id', 
        write_only=True
    )

    class Meta:
        model = Medicine
        # Explicitly list fields, excluding the auto-generated FK field
        fields = [
            'medicine_id', 'medicine_name', 'manufacturing_date', 
            'expiry_date', 'price', 'medicine_category_id'
        ]
        # Important: The foreign key field (medicine_category) is implicitly included 
        # when using a custom field like 'medicine_category_id' as source.
        # We must map the custom input field back to the model field in create/update methods
        # or use simpler approaches like SlugRelatedField. 
        # Let's simplify and use the primary key approach for better REST compliance:

class Medicine_CreateUpdateSerializer(serializers.ModelSerializer):
    """Simplified for POST/PUT/PATCH - uses the PK for Foreign Key writes."""
    class Meta:
        model = Medicine
        fields = '__all__'
        extra_kwargs = {
            # Make sure the FK field is writable
            'medicine_category': {'write_only': True} 
        }


# --- 3. MEDICINE STOCK SERIALIZERS ---

class MedicineStock_ReadSerializer(serializers.ModelSerializer):
    """For GET requests: shows nested medicine details."""
    medicine = SimpleMedicineSerializer(read_only=True)
    
    class Meta:
        model = MedicineStock
        fields = '__all__'

class MedicineStock_WriteSerializer(serializers.ModelSerializer):
    """For POST/PUT requests: expects only the Medicine ID."""
    class Meta:
        model = MedicineStock
        fields = '__all__'
        extra_kwargs = {
            'medicine': {'write_only': True}
        }


# --- 4. MEDICINE PRESCRIPTION SERIALIZERS ---

class AppointmentForPrescriptionSerializer(serializers.ModelSerializer):
    """A minimal serializer for the appointment to nest within prescription."""
    patient = SimplePatientSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'appointment_date', 'patient']

class MedicinePrescription_ReadSerializer(serializers.ModelSerializer):
    """
    For GET requests: shows nested details for Medicine and Appointment.
    This replaces the potentially slow 'depth=1'.
    """
    medicine = SimpleMedicineSerializer(read_only=True)
    appointment = AppointmentForPrescriptionSerializer(read_only=True)
    
    class Meta:
        model = MedicinePrescription
        fields = '__all__'

class MedicinePrescription_WriteSerializer(serializers.ModelSerializer):
    """For POST/PUT requests: expects only the IDs for Foreign Keys."""
    class Meta:
        model = MedicinePrescription
        fields = '__all__'
        extra_kwargs = {
            # Ensure only the IDs are needed for these fields when writing
            'medicine': {'write_only': True},
            'appointment': {'write_only': True},
        }