from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctorUser
from .serializers import (
    AppointmentDetailSerializer, ConsultationSerializer, LabReportDetailSerializer,
    PrescriptionSerializer, LabPrescriptionSerializer, SimpleMedicineSerializer, SimpleLabTestSerializer
)
from apibackendapp.models import (
    Appointment, Consultation, Medicine, LabTest, LabTestReport, 
    MedicinePrescription, LabTestPrescription, Doctor
)
from apibackendapp.permissions import IsDoctor

class DoctorAppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (Read-Only) Viewset for a Doctor to see THEIR appointments.
    """
    serializer_class = AppointmentDetailSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def get_queryset(self):
        # Get the Doctor profile linked to the logged-in user
        doctor = Doctor.objects.get(user=self.request.user)
        # Return only appointments assigned to this doctor
        return Appointment.objects.filter(doctor=doctor)

class ConsultationViewSet(viewsets.ModelViewSet):
    """
    (CRUD) Viewset for a Doctor to manage Consultations.
    """
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def get_queryset(self):
        # A Doctor can only see consultations they created
        doctor = Doctor.objects.get(user=self.request.user)
        return Consultation.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        # Automatically assign the logged-in doctor when creating
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)

class MedicineListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (Read-Only) Viewset for Doctors to see all available Medicines.
    """
    queryset = Medicine.objects.all()
    serializer_class = SimpleMedicineSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

class LabTestListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (Read-Only) Viewset for Doctors to see all available Lab Tests.
    """
    queryset = LabTest.objects.all()
    serializer_class = SimpleLabTestSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

class LabReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    (Read-Only) Viewset for a Doctor to see Lab Reports for THEIR patients.
    """
    serializer_class = LabReportDetailSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def get_queryset(self):
        # Get the Doctor profile
        doctor = Doctor.objects.get(user=self.request.user)
        
        # Get IDs of all patients who have an appointment with this doctor
        my_patient_ids = Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True).distinct()
        
        # Return reports for those patients
        return LabTestReport.objects.filter(patient_id__in=my_patient_ids)

class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    (CRUD) Viewset for a Doctor to manage Medicine Prescriptions.
    """
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def get_queryset(self):
        # A Doctor can only see prescriptions they created
        doctor = Doctor.objects.get(user=self.request.user)
        return MedicinePrescription.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        # Automatically assign the logged-in doctor
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)

class LabPrescriptionViewSet(viewsets.ModelViewSet):
    """
    (CRUD) Viewset for a Doctor to manage Lab Test Prescriptions.
    """
    serializer_class = LabPrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def get_queryset(self):
        # A Doctor can only see lab prescriptions they created
        doctor = Doctor.objects.get(user=self.request.user)
        return LabTestPrescription.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        # Automatically assign the logged-in doctor
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)

class DoctorOnlyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor, IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = None  # Define appropriate serializer

    def get_serializer_class(self):
        # Return the appropriate serializer for Doctor
        pass
    def get_queryset(self):
        # A Doctor can only see their own profile
        doctor = Doctor.objects.get(user=self.request.user)
        return Doctor.objects.filter(id=doctor.id)