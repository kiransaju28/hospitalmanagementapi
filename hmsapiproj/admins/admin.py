from django.contrib import admin
from .models import Department, Staff, Doctor

# Register your models here.
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Doctor)