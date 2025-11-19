from rest_framework import serializers
from apibackendapp.models import (
    Appointment, Consultation, Medicine, LabTest, LabTestReport, 
    MedicinePrescription, LabTestPrescription, Patient, Doctor
)

# --- Helper Serializers (for Read-Only nested data) ---

class SimplePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'fullname', 'mobileno', 'gender']

class SimpleDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name']

class SimpleMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['medicine_id', 'name', 'manufacturer', 'description']

class SimpleLabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['test_id', 'name', 'description']

# --- Main Serializers ---

class AppointmentDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for a Doctor to VIEW their appointments.
    """
    patient = SimplePatientSerializer(read_only=True)
    doctor = SimpleDoctorSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient', 'doctor', 'appointment_date', 'status', 'reason']

class ConsultationSerializer(serializers.ModelSerializer):
    """
    CRUD serializer for Consultations.
    Doctor field is set automatically from the view.
    """
    class Meta:
        model = Consultation
        fields = ['consultation_id', 'patient', 'appointment', 'notes', 'diagnosis', 'created_at']
        # 'doctor' is read-only because it's set in the view
        read_only_fields = ['consultation_id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make patient/appointment writable on create/update
        # but use nested serializer on read
        if self.context.get('request') and self.context['request'].method in ['GET']:
            self.fields['patient'] = SimplePatientSerializer(read_only=True)
        else:
            self.fields['patient'] = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
            self.fields['appointment'] = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all())

class LabReportDetailSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for a Doctor to VIEW patient lab reports.
    """
    patient = SimplePatientSerializer(read_only=True)
    test = SimpleLabTestSerializer(read_only=True)
    
    class Meta:
        model = LabTestReport
        fields = ['report_id', 'patient', 'test', 'report_file', 'report_date', 'notes']

class PrescriptionSerializer(serializers.ModelSerializer):
    """
    CRUD serializer for Medicine Prescriptions.
    Doctor field is set automatically from the view.
    """
    class Meta:
        model = MedicinePrescription
        fields = ['prescription_id', 'patient', 'medicine', 'dosage', 'frequency', 'duration', 'notes', 'created_at']
        read_only_fields = ['prescription_id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method in ['GET']:
            self.fields['patient'] = SimplePatientSerializer(read_only=True)
            self.fields['medicine'] = SimpleMedicineSerializer(read_only=True)
        else:
            self.fields['patient'] = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
            self.fields['medicine'] = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())

class LabPrescriptionSerializer(serializers.ModelSerializer):
    """
    CRUD serializer for Lab Test Prescriptions.
    Doctor field is set automatically from the view.
    """
    class Meta:
        model = LabTestPrescription
        fields = ['lab_prescription_id', 'patient', 'lab_test', 'notes', 'created_at']
        read_only_fields = ['lab_prescription_id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method in ['GET']:
            self.fields['patient'] = SimplePatientSerializer(read_only=True)
            self.fields['lab_test'] = SimpleLabTestSerializer(read_only=True)
        else:
            self.fields['patient'] = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
            self.fields['lab_test'] = serializers.PrimaryKeyRelatedField(queryset=LabTest.objects.all())