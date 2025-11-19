from rest_framework import viewsets
from admins.permissions import Islabtec
from .models import (
    LabTestCategory, LabTestParameter, LabReport, LabReportResult, LabBill, LabBillItem
)
from .serializers import (
    LabTestCategorySerializer, LabTestParameterSerializer, 
    LabReportSerializer, LabReportResultSerializer, 
    LabBillSerializer, LabBillItemSerializer
)
from doctor.models import LabTestOrder
from doctor.serializers import LabTestOrderSerializer

# 1. RESTRICTED VIEWS (Read-Only for Technician)
class LabTestCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Technician can VIEW test types, but NOT create/edit them. """
    permission_classes = [Islabtec]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer

class LabTestParameterViewSet(viewsets.ReadOnlyModelViewSet):
    """ Technician can VIEW parameters, but NOT create/edit them. """
    permission_classes = [Islabtec]
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer

# 2. WORKFLOW VIEWS (Full Access)

class PendingLabTestsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Shows all LabTestOrders from doctors.
    This acts as the Technician's "To-Do List".
    """
    permission_classes = [Islabtec]
    queryset = LabTestOrder.objects.all().order_by('-id')
    serializer_class = LabTestOrderSerializer

class LabReportViewSet(viewsets.ModelViewSet):
    """ Create Reports (Technician's main job) """
    permission_classes = [Islabtec]
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer

class LabReportResultViewSet(viewsets.ModelViewSet):
    permission_classes = [Islabtec]
    queryset = LabReportResult.objects.all()
    serializer_class = LabReportResultSerializer

class LabBillViewSet(viewsets.ModelViewSet):
    """ Create Bills (Separate from Report) """
    permission_classes = [Islabtec]
    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer

class LabBillItemViewSet(viewsets.ModelViewSet):
    permission_classes = [Islabtec]
    queryset = LabBillItem.objects.all()
    serializer_class = LabBillItemSerializer