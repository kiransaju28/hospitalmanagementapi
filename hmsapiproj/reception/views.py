from rest_framework import viewsets, filters
from .models import Patient, Appointment, ConsultationBill
from .serializers import PatientSerializer, AppointmentSerializer, ConsultationBillSerializer

# --- 1. Import the Custom Permission ---
from admins.permissions import Isreception

class PatientViewSet(viewsets.ModelViewSet):
    # --- 2. Apply the Permission ---
    permission_classes = [Isreception]
    
    queryset = Patient.objects.all().order_by("id")
    serializer_class = PatientSerializer

    # Enable search only for name and phone
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient_name', 'phone']

class AppointmentViewSet(viewsets.ModelViewSet):
    # --- 2. Apply the Permission ---
    permission_classes = [Isreception]
    
    queryset = Appointment.objects.all().order_by('-id')
    serializer_class = AppointmentSerializer

    # Search API (Search by token or patient name)
    filter_backends = [filters.SearchFilter]
    search_fields = ['token', 'patient__patient_name']

class ConsultationBillViewSet(viewsets.ModelViewSet):
    # --- 2. Apply the Permission ---
    permission_classes = [Isreception]
    
    queryset = ConsultationBill.objects.all().order_by('-id')
    serializer_class = ConsultationBillSerializer

    # Enable searching
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name', 'appointment__token']