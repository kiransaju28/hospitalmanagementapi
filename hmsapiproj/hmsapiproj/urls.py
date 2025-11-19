"""
URL configuration for clinic_project project.
"""
from django.contrib import admin
from django.urls import path, include

# --- Import these two views for JWT Login ---
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- ADD THESE FOR API LOGIN ---
    # This creates the URL: /api/token/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # This creates the URL: /api/token/refresh/
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # --------------------------------

    # --- Your App URLs ---
    path('api/admins/', include('admins.urls')), # Correct
    path('api/doctor/', include('doctor.urls')),           # <-- ADDED YOUR DOCTOR APP
    
    # Your teammates will add their apps here later
    path('api/reception/', include('reception.urls')),
    path('api/lab/', include('labtec.urls')),
    path('api/pharmacist/', include('pharmacist.urls')),
]
