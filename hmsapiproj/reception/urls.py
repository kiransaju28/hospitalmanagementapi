# reception/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet

# 1. Create a router instance
router = DefaultRouter()

# 2. Register the ViewSets
# This automatically generates URLs like:
# /patients/ (GET: list, POST: create)
# /patients/{pk}/ (GET: retrieve, PUT/PATCH: update, DELETE: destroy)
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

# 3. Define the urlpatterns
# The router includes all generated URLs under the base path
urlpatterns = [
    path('', include(router.urls)),
]
