from rest_framework import serializers
from apibackendapp.models import (
    Patient,
    Doctor,
    Specialization,
    Appointment,
    Billing
    # You might also need: Billing, Staff, etc.
)


# --- Nested Serializers for Read Operations ---

class SpecializationSerializer(serializers.ModelSerializer):
    """Minimal serializer for Doctor lookup."""
    class Meta:
        model = Specialization
        fields = ['specialization_name']


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Doctors. The receptionist needs this
    to select a doctor when creating an appointment.
    """
    specialization = SpecializationSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'doctor_id',
            'name',
            'contact_info',
            'consultation_fee',
            'specialization',
        ]
        read_only_fields = ['doctor_id']


# --- Patient Serializers (Primary Reception Duty) ---

class PatientSerializer(serializers.ModelSerializer):
    """
    Handles all CRUD operations for Patient records (registration and updates).
    """
    class Meta:
        model = Patient
        fields = [
            'patient_id',
            'patient_name',
            'date_of_birth',
            'gender',
            'contact_info',
            'address',
            'blood_group',
        ]
        read_only_fields = ['patient_id']


# --- Appointment Serializers (Primary Reception Duty) ---

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    Used for creating a new appointment. Requires IDs for foreign keys.
    """
    # The fields patient_id and doctor_id will be expected in the POST data.
    # We use ModelSerializer which automatically handles the relation fields
    # (patient, doctor) when provided with the respective primary keys (PKs).

    class Meta:
        model = Appointment
        fields = [
            'appointment_id',
            'appointment_date',
            'token_number',
            'patient', # Expects Patient PK (e.g., 'P001')
            'doctor',  # Expects Doctor PK (e.g., 'D001')
        ]
        # Make consultation_status read-only for creation
        read_only_fields = ['consultation_status','appointment_id']


class AppointmentDetailSerializer(serializers.ModelSerializer):
    """
    Used for retrieving and viewing appointment details,
    including nested Patient and Doctor information.
    """
    patient = PatientSerializer(read_only=True)
    # We use DoctorListSerializer for embedded doctor info
    doctor = DoctorListSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'appointment_id',
            'appointment_date',
            'token_number',
            'consultation_status',
            'patient',
            'doctor',
        ]
class BillingSerializer(serializers.ModelSerializer):
    """
    Serializer for Billing records.
    Receptionists may need to view billing info.
    """
    appointment = AppointmentDetailSerializer(read_only=True)

    class Meta:
        model = Billing
        fields = [
            'bill_id',
            'appointment',
            'amount',
            'billing_date',
            'payment_status',
        ]
    read_only_fields = ['amount', 'billing_date']