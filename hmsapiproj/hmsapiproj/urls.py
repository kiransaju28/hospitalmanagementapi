# hmsapiproj/urls.py (CLEANED UP)

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. JWT Authentication Endpoints (for login/refresh)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 2. Application API Endpoints (Admin and Reception)
    path('api/admins/', include('admins.urls')),
    
    # 3. Reception API Endpoints (The correct, single entry)
    path('api/reception/', include('reception.urls')),
]