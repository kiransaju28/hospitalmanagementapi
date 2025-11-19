from rest_framework import serializers
from .models import BasicVitals, Consultation, PrescriptionItem, LabTestOrder
from labtec.models import LabReport, LabReportResult
from reception.models import Patient

# --- STANDARD SERIALIZERS ---

class PrescriptionItemSerializer(serializers.ModelSerializer):
    # We use this for reading (showing the name)
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    
    class Meta:
        model = PrescriptionItem
        # FIX: Added 'consultation' and 'medicine' so you can save them!
        fields = ['id', 'consultation', 'medicine', 'medicine_name', 'dosage', 'frequency', 'duration']

class LabTestOrderSerializer(serializers.ModelSerializer):
    # We use this for reading (showing the name)
    test_name = serializers.CharField(source='test.category_name', read_only=True)
    
    class Meta:
        model = LabTestOrder
        # FIX: Added 'consultation' and 'test' so you can save them!
        fields = ['id', 'consultation', 'test', 'test_name']

class BasicVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicVitals
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    # These show the details nested inside the consultation view
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'appointment', 'vitals', 'symptoms', 'diagnosis', 'notes',
            'fulfill_pharmacist_internally', 'fulfill_lab_internally',
            'prescription_items', 'lab_test_orders'
        ]

# --- HISTORY SERIALIZERS (For Patient History View) ---

class LabReportResultHistorySerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source='parameter.label')
    normal_range = serializers.CharField(source='parameter.normal_range')
    class Meta:
        model = LabReportResult
        fields = ['parameter_name', 'value', 'normal_range']

class LabReportHistorySerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='category.category_name')
    results = LabReportResultHistorySerializer(many=True, read_only=True)
    class Meta:
        model = LabReport
        fields = ['id', 'test_name', 'report_date', 'remarks', 'results']

class ConsultationHistorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='appointment.doctor.staff.full_name', read_only=True)
    visit_date = serializers.DateTimeField(source='appointment.appointment_date', read_only=True)
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'doctor_name', 'visit_date', 'symptoms', 
            'diagnosis', 'notes', 'prescription_items', 'lab_test_orders'
        ]

class PatientHistorySerializer(serializers.ModelSerializer):
    """
    DOCTOR VIEW: Shows Consultations and Lab Reports.
    DOES NOT SHOW BILLS.
    """
    consultations = serializers.SerializerMethodField()
    lab_reports = LabReportHistorySerializer(many=True, read_only=True, source='labreport_set')
    
    class Meta:
        model = Patient
        fields = [
            'id', 'patient_name', 'age', 'gender', 'blood_group',
            'consultations', 'lab_reports' 
        ]

    def get_consultations(self, obj):
        consults = Consultation.objects.filter(appointment__patient=obj).order_by('-id')
        return ConsultationHistorySerializer(consults, many=True).data