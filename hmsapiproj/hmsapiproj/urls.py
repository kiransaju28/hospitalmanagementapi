from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('labtec/', include('labtec.urls')),
    path('api/', include('apibackendapp.urls')),
]
