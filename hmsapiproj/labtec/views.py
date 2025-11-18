from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apibackendapp.models import (
    LabTest, LabTestPrescription, LabTestReport,
)
from .serializers import (
    LabTestSerializer,
    LabTestPrescriptionSerializer,
    LabTestReportSerializer,
)

# -----------------------
# LAB TEST CRUD
# -----------------------

class LabTestListCreateView(generics.ListCreateAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


class LabTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


# -----------------------
# LAB PRESCRIPTION CRUD
# -----------------------

from rest_framework.exceptions import PermissionDenied

class LabTestPrescriptionView(generics.ListAPIView):
    """
    Doctor creates prescriptions (only via backend)
    Lab Technician can only view, not create.
    """
    queryset = LabTestPrescription.objects.all()
    serializer_class = LabTestPrescriptionSerializer



class LabTestPrescriptionDetailView(generics.RetrieveAPIView):
    """
    Lab Technician can only view individual prescription.
    No edits allowed.
    """
    queryset = LabTestPrescription.objects.all()
    serializer_class = LabTestPrescriptionSerializer



# -----------------------
# LAB REPORT GENERATION
# -----------------------

class LabReportView(APIView):
    def get(self, request, pk):
        try:
            report = LabTestReport.objects.get(report_id=pk)
            serializer = LabTestReportSerializer(report)
            return Response(serializer.data)
        except LabTestReport.DoesNotExist:
            return Response({"error": "Report not found"}, status=404)
