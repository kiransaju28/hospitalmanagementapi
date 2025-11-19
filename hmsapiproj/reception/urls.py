from rest_framework.routers import DefaultRouter
from .views import PatientViewSet,AppointmentViewSet,ConsultationBillViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'bills', ConsultationBillViewSet, basename='bills')

urlpatterns = router.urls
