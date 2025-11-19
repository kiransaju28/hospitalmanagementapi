from rest_framework import serializers
from datetime import date
from .models import Patient,Appointment,ConsultationBill
from admins.models import Doctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "patient_name",
            "age",
            "email",
            "date_of_birth",
            "blood_group",
            "gender",
            "address",
            "phone",
        ]
        read_only_fields = ["age"]  # age is auto-calculated

    # -----------------------------------------
    # FIELD-LEVEL VALIDATION
    # -----------------------------------------

    # 1️⃣ BLOOD GROUP VALIDATION
    def validate_blood_group(self, value):
        valid_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        if value.upper() not in valid_groups:
            raise serializers.ValidationError("Invalid blood group.")

        return value.upper()

    # 2️⃣ GENDER VALIDATION
    def validate_gender(self, value):
        valid = ["male", "female", "other"]

        if value.lower() not in valid:
            raise serializers.ValidationError(
                "Gender must be Male, Female, or Other."
            )

        return value.capitalize()

    # 3️⃣ PHONE VALIDATION
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain only digits.")

        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")

        return value

    # -----------------------------------------
    # OBJECT-LEVEL VALIDATION
    # -----------------------------------------
    def validate(self, data):
        dob = data.get("date_of_birth")

        # Age calculation
        if dob:
            today = date.today()
            age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
            )

            if age < 0:
                raise serializers.ValidationError("Date of birth cannot be in the future.")

            data["age"] = age

        return data

    # -----------------------------------------
    # CREATE PATIENT (AGE AUTO INSERTED)
    # -----------------------------------------
    def create(self, validated_data):
        # age is already inserted in validated_data
        return Patient.objects.create(**validated_data)

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['id', 'token', 'appointment_date', 'status', 'patient', 'doctor']
        read_only_fields = ['token', 'appointment_date', 'status']

    # ---------- AUTO TOKEN GENERATOR ----------
    def generate_token(self):
        last = Appointment.objects.order_by('-id').first()
        if not last:
            return "T001"
        last_num = int(last.token[1:])  # Remove T and convert
        new_num = last_num + 1
        return f"T{new_num:03d}"  # Format T003

    def validate(self, attrs):

        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        # ---- Validate Patient Exists ----
        if not Patient.objects.filter(id=patient.id).exists():
            raise serializers.ValidationError("Patient does not exist.")

        # ---- Validate Doctor Exists ----
        if not Doctor.objects.filter(id=doctor.id).exists():
            raise serializers.ValidationError("Doctor does not exist.")

        # ---- Prevent double booking of patient same day ----
        from django.utils import timezone
        today = timezone.now().date()

        if Appointment.objects.filter(patient=patient, appointment_date__date=today).exists():
            raise serializers.ValidationError("This patient already has an appointment today.")

        # # ---- Prevent double booking of doctor same day ----
        # if Appointment.objects.filter(doctor=doctor, appointment_date__date=today).exists():
        #     raise serializers.ValidationError("Doctor is already booked today.")

        return attrs

    def create(self, validated_data):
        validated_data['token'] = self.generate_token()
        validated_data['status'] = "Scheduled"
        return super().create(validated_data)

class ConsultationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = ['id', 'appointment', 'patient', 'bill_date', 'amount']
        read_only_fields = ['patient', 'bill_date', 'amount']

    def validate(self, attrs):
        appointment = attrs.get('appointment')

        # Check if appointment exists
        if not appointment:
            raise serializers.ValidationError("Appointment is required.")

        # Prevent duplicate bill
        if ConsultationBill.objects.filter(appointment=appointment).exists():
            raise serializers.ValidationError("Bill already generated for this appointment.")

        # Check if doctor exists
        if not appointment.doctor:
            raise serializers.ValidationError("Doctor not assigned to this appointment.")

        return attrs

    def create(self, validated_data):
        appointment = validated_data['appointment']

        # Auto-set values
        patient = appointment.patient
        amount = appointment.doctor.consultation_fee  # From Doctor model

        bill = ConsultationBill.objects.create(
            appointment=appointment,
            patient=patient,
            amount=amount
        )
        return bill
