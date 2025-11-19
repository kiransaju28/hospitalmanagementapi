# In labtec/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LabTestCategoryViewSet, LabTestParameterViewSet, 
    LabReportViewSet, LabReportResultViewSet, 
    LabBillViewSet, LabBillItemViewSet,
    PendingLabTestsViewSet # <-- Add this
)

router = DefaultRouter()
router.register(r'test-categories', LabTestCategoryViewSet)
router.register(r'test-parameters', LabTestParameterViewSet)
router.register(r'lab-reports', LabReportViewSet)
router.register(r'lab-report-results', LabReportResultViewSet)
router.register(r'lab-bills', LabBillViewSet)
router.register(r'lab-bill-items', LabBillItemViewSet)
router.register(r'pending-tests', PendingLabTestsViewSet, basename='pending-tests') # <-- Add this

urlpatterns = [
    path('', include(router.urls)),
]
