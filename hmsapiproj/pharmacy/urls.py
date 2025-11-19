from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicineCategoryViewSet, 
    MedicineViewSet, 
    MedicineStockViewSet, 
    MedicinePrescriptionViewSet
)

router = DefaultRouter()
router.register(r'categories', MedicineCategoryViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'stock', MedicineStockViewSet)
router.register(r'prescriptions', MedicinePrescriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]