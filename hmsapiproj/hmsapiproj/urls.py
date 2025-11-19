# hmsapiproj/urls.py (CLEANED UP)

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include('admins.urls')),
    path('login/', include('admins.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('apibackendapp.urls')),
    path('api/doctor/', include('doctor.urls')),
    path('api/admins/', include('admins.urls')),
    path('api/reception/', include('reception.urls')),
    path('api/labtec/', include('labtec.urls')),    
    path('api/pharmacy/', include('pharmacy.urls')),
]
