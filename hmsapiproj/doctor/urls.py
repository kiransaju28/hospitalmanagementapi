from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Read-Only Views
router.register(r'my-appointments', views.DoctorAppointmentViewSet, basename='doctor-appointments')
router.register(r'lab-reports', views.LabReportViewSet, basename='doctor-lab-reports')
router.register(r'medicines-list', views.MedicineListViewSet, basename='medicines-list')
router.register(r'lab-tests-list', views.LabTestListViewSet, basename='lab-tests-list')

# CRUD Views
router.register(r'consultations', views.ConsultationViewSet, basename='doctor-consultations')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='doctor-prescriptions')
router.register(r'lab-prescriptions', views.LabPrescriptionViewSet, basename='doctor-lab-prescriptions')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]