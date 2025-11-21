# In admins/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    StaffViewSet,
    DoctorViewSet,
    AdminPatientHistoryViewSet,
    AdminLabTestCategoryViewSet,
    AdminLabTestParameterViewSet
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)

# The router automatically creates all the ViewSet URLs
router = DefaultRouter()
#router.register(r'departments', DepartmentViewSet, basename='departments') # <-- NEW: Add this line
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'doctors', DoctorViewSet, basename='doctors')
router.register(r'patient-history', AdminPatientHistoryViewSet, basename='admin-patient-history')
router.register(r'manage-lab-tests', AdminLabTestCategoryViewSet, basename='manage-lab-tests')
router.register(r'manage-lab-parameters', AdminLabTestParameterViewSet, basename='manage-lab-parameters')

urlpatterns = [
    # Include all the router URLs
    path('', include(router.urls)),
    
    # Manually add the user registration URL
    path('register-user/', UserRegistrationView.as_view(), name='register-user'),
]