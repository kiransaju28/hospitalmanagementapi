from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BasicVitalsViewSet, 
    ConsultationViewSet, 
    PrescriptionItemViewSet, 
    LabTestOrderViewSet,
    MyTodayAppointmentsViewSet,  # <-- Imported
    PatientHistoryView           # <-- Imported
)

router = DefaultRouter()
router.register(r'basic-vitals', BasicVitalsViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'prescription-items', PrescriptionItemViewSet)
router.register(r'lab-test-orders', LabTestOrderViewSet)
# This creates the URL: /api/doctor/my-today-appointments/
router.register(r'my-today-appointments', MyTodayAppointmentsViewSet, basename='my-today-appointments')

urlpatterns = [
    path('', include(router.urls)),
    
    # This creates the URL: /api/doctor/patient-history/<id>/
    path(
        'patient-history/<int:id>/', 
        PatientHistoryView.as_view(), 
        name='patient-history'
    ),
    
]