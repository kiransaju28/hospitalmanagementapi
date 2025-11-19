from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

# Adjust imports based on your project structure
from apibackendapp.models import (
    MedicineCategory,
    Medicine,
    MedicineStock,
    MedicinePrescription
)
from .serializers import (
    MedicineCategorySerializer, 
    # Read/Write Serializers for Medicine
    Medicine_ReadSerializer, 
    Medicine_CreateUpdateSerializer, 
    # Read/Write Serializers for Stock
    MedicineStock_ReadSerializer, 
    MedicineStock_WriteSerializer, 
    # Read/Write Serializers for Prescription
    MedicinePrescription_ReadSerializer, 
    MedicinePrescription_WriteSerializer
)

# Assuming 'IsMedicalStaff' and 'IsAuthenticated' are correctly defined elsewhere.
# If 'IsMedicalStaff' covers all necessary permissions (Admin, Pharmacist, Doctor), use it.
# from .permissions import IsMedicalStaff 

# --- Base ViewSet for Read/Write Separation ---

class MultipleSerializerMixin:
    """
    Mixin to set different serializers for different HTTP actions.
    Requires serializer_classes attribute to be set on the ViewSet.
    Example: serializer_classes = {'list': ListSerializer, 'create': CreateSerializer}
    """
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


# --- PHARMACY MANAGEMENT VIEWSETS ---
# These viewsets primarily handle inventory and category management.

class MedicineCategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Medicine Categories. 
    Category management is typically restricted to staff/admins.
    """
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    # Ensure only authorized staff can manage categories
    # permission_classes = [IsMedicalStaff] 
    
    # NOTE: Using a placeholder permission class if 'IsMedicalStaff' isn't available
    permission_classes = [IsAuthenticated] 


class MedicineViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    Handles CRUD for Medicine definitions (e.g., price, dates, category).
    Uses separate serializers for detailed reads and simple writes.
    """
    queryset = Medicine.objects.all()
    
    # Default serializer (used for unsupported actions or if action not in dict)
    serializer_class = Medicine_ReadSerializer 
    
    # Map actions to specific serializers
    serializer_classes = {
        'list': Medicine_ReadSerializer,
        'retrieve': Medicine_ReadSerializer,
        'create': Medicine_CreateUpdateSerializer,
        'update': Medicine_CreateUpdateSerializer,
        'partial_update': Medicine_CreateUpdateSerializer,
    }
    
    # permission_classes = [IsMedicalStaff]
    permission_classes = [IsAuthenticated]


class MedicineStockViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    Handles CRUD for medicine stock levels.
    """
    queryset = MedicineStock.objects.all()
    serializer_class = MedicineStock_ReadSerializer # Default to read serializer
    
    serializer_classes = {
        'list': MedicineStock_ReadSerializer,
        'retrieve': MedicineStock_ReadSerializer,
        # Use write serializer for creating/updating stock
        'create': MedicineStock_WriteSerializer,
        'update': MedicineStock_WriteSerializer,
        'partial_update': MedicineStock_WriteSerializer,
    }
    
    # permission_classes = [IsMedicalStaff]
    permission_classes = [IsAuthenticated]


# --- PRESCRIPTION VIEWSET ---

class MedicinePrescriptionViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    """
    Viewset for prescriptions. 
    Doctors create prescriptions; Pharmacists read and update them (e.g., set dispensed status).
    """
    queryset = MedicinePrescription.objects.all()
    # Default serializer
    serializer_class = MedicinePrescription_ReadSerializer 
    
    serializer_classes = {
        'list': MedicinePrescription_ReadSerializer,
        'retrieve': MedicinePrescription_ReadSerializer,
        # Write operations require only FK IDs
        'create': MedicinePrescription_WriteSerializer,
        'update': MedicinePrescription_WriteSerializer,
        'partial_update': MedicinePrescription_WriteSerializer,
    }
    
    # Keep IsAuthenticated as a base, but ideally, you'd use a custom permission
    # that checks if the user is a Doctor (for POST) or a Pharmacist (for GET/PUT).
    permission_classes = [IsAuthenticated]