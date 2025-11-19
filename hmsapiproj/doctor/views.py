from rest_framework import viewsets, generics
from .models import BasicVitals, Consultation, PrescriptionItem, LabTestOrder
from .serializers import (
    BasicVitalsSerializer, 
    ConsultationSerializer, 
    PrescriptionItemSerializer, 
    LabTestOrderSerializer,
    PatientHistorySerializer
)
from admins.permissions import IsDoctor
import datetime
from reception.models import Appointment, Patient
from reception.serializers import AppointmentSerializer 

class MyTodayAppointmentsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Shows the logged-in doctor THEIR appointments for TODAY.
    """
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        today = datetime.date.today()
        
        # Safety check: Is this user actually a doctor?
        if not hasattr(user, 'staff') or not hasattr(user.staff, 'doctor'):
             return Appointment.objects.none()

        # Filter: Appointments for THIS doctor on THIS day
        return Appointment.objects.filter(
            doctor=user.staff.doctor, 
            appointment_date__date=today
        ).order_by('appointment_date')

class PatientHistoryView(generics.RetrieveAPIView):
    """
    Shows complete medical history for one patient.
    """
    permission_classes = [IsDoctor]
    queryset = Patient.objects.all()
    serializer_class = PatientHistorySerializer
    lookup_field = 'id' 

# --- STANDARD CRUD VIEWS ---

class BasicVitalsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = BasicVitals.objects.all()
    serializer_class = BasicVitalsSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer

class LabTestOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = LabTestOrder.objects.all()
    serializer_class = LabTestOrderSerializer