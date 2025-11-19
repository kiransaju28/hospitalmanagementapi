# In admins/views.py

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .permissions import IsAdmin  # Use our new Admin permission
from .serializers import UserRegistrationSerializer, StaffDetailSerializer, DoctorDetailSerializer
from .models import Staff, Doctor

# --- Imports from other apps ---
# We need the models and serializers to re-use them
from reception.models import Patient
from labtec.models import LabTestCategory, LabTestParameter
from doctor.serializers import PatientHistorySerializer 
from labtec.serializers import LabTestCategorySerializer, LabTestParameterSerializer 


class UserRegistrationView(generics.CreateAPIView):
    """
    Endpoint for an Admin to create a new User, Staff, and (if applicable) Doctor.
    URL: /api/admins/register-user/
    """
    permission_classes = [IsAdmin]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": f"User '{user.username}' created successfully as a {request.data['role']}."},
            status=status.HTTP_201_CREATED
        )

class StaffViewSet(viewsets.ModelViewSet):
    """ Read-only endpoint for viewing all staff. """
    permission_classes = [IsAdmin]
    queryset = Staff.objects.all()
    serializer_class = StaffDetailSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """ Read-only endpoint for viewing all doctors. """
    permission_classes = [IsAdmin]
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer, StaffSerializer, DoctorSerializer, 
    DepartmentSerializer, AdminPatientHistorySerializer 
)
from .models import Staff, Doctor, Department
from reception.models import Patient
from labtec.models import LabTestCategory, LabTestParameter
from labtec.serializers import LabTestCategorySerializer, LabTestParameterSerializer 

# ... (User Registration, Staff, Doctor, Department views stay the same) ...

class AdminPatientHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for admins.
    Shows Medical History + BILLING HISTORY.
    """
    permission_classes = [IsAdmin]
    queryset = Patient.objects.all()
    serializer_class = AdminPatientHistorySerializer # <-- Uses the serializer WITH bills

class AdminLabTestCategoryViewSet(viewsets.ModelViewSet):
    """
    FULL CONTROL: Admin can Create, Update, Delete Lab Tests.
    """
    permission_classes = [IsAdmin]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer 

class AdminLabTestParameterViewSet(viewsets.ModelViewSet):
    """
    FULL CONTROL: Admin can Create, Update, Delete Parameters.
    """
    permission_classes = [IsAdmin]
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer