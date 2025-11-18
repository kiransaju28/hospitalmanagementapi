from django.urls import path
from .views import (
    LabTestListCreateView,
    LabTestDetailView,
    LabTestPrescriptionView,
    LabTestPrescriptionDetailView,
    LabReportView,
)

urlpatterns = [
    path('labtests/', LabTestListCreateView.as_view(), name="labtest-list"),
    path('labtests/<str:pk>/', LabTestDetailView.as_view(), name="labtest-detail"),

    path('prescriptions/', LabTestPrescriptionView.as_view(), name="labtest-prescription"),
    path('prescriptions/<str:pk>/', LabTestPrescriptionDetailView.as_view(), name="labtest-prescription-detail"),

    path('report/<str:pk>/', LabReportView.as_view(), name="labtest-report"),
]
