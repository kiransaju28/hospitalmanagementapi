from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import viewsets
from apibackendapp.models import Patient, Doctor, Appointment
from .serializers import (
    PatientSerializer,
    DoctorListSerializer,
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
)
from .permissions import IsReceptionStaff, IsDoctorReadOnly

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Patients to be viewed or edited (Registered/Updated).
    Receptionists handle new patient registration and profile updates.
    """
    # 1. Fetch all Patient objects
    queryset = Patient.objects.all().order_by('patient_name')
    
    # 2. Use the standard PatientSerializer for all actions (list, create, retrieve, update)
    serializer_class = PatientSerializer

    permission_classes = [IsAuthenticated, IsReceptionStaff]  # You can add custom permissions here if needed


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Doctors to be viewed.
    Receptionists need this for scheduling appointments. This is read-only.
    """
    # 1. Fetch all Doctor objects and pre-fetch the related Specialization for efficiency
    queryset = Doctor.objects.all().select_related('specialization').order_by('name')
    
    # 2. Use the minimal DoctorListSerializer
    serializer_class = DoctorListSerializer
    
    # You could optionally add a search filter here, e.g., to filter by specialization
    ermission_classes = [IsAuthenticated, IsDoctorReadOnly]


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Appointments to be viewed, created, or updated.
    Receptionists manage the appointment scheduling process.
    """
    # 1. Fetch all Appointments and pre-fetch Patient and Doctor details
    #    (and Doctor's Specialization) for efficient detail retrieval.
    queryset = Appointment.objects.all().select_related('patient', 'doctor', 'doctor__specialization').order_by('-appointment_date')

    # 2. Override get_serializer_class to use different serializers for different actions
    def get_serializer_class(self):
        """
        Returns the correct serializer based on the action requested.
        - Uses Detail serializer for GET (list/retrieve) to embed patient/doctor data.
        - Uses Create serializer for POST/PUT/PATCH (create/update) to accept simple FKs (IDs).
        """
        if self.action in ['list', 'retrieve']:
            return AppointmentDetailSerializer
        # create, update, partial_update
        return AppointmentCreateSerializer
    
    permission_classes = [IsAuthenticated, IsReceptionStaff]

    # 3. Optional: Add a method to calculate and assign the token number automatically
    #    This is best handled in a custom manager or the serializer's create method,
    #    but for a simple view, we can demonstrate it here.
    def perform_create(self, serializer):
        # Example logic to find the next token number for the day
        current_date = serializer.validated_data['appointment_date'].date()
        next_token = Appointment.objects.filter(appointment_date__date=current_date).count() + 1
        serializer.save(token_number=next_token)
        serializer.save()

