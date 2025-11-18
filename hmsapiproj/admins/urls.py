from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    StaffViewSet, 
    SpecializationViewSet, 
    DoctorViewSet
)

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
# Removed 'roles' and 'users' (SystemUser)
router.register(r'staff', StaffViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'all-users', views.UserViewSet) # Renamed to avoid confusion

urlpatterns=[
    path("signup/", views.SignupApiView.as_view(), name="user-signup"),
    path("login/", views.LoginAPIView.as_view(), name="user-login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls