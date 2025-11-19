from rest_framework import permissions
from django.contrib.auth.models import User 
from apibackendapp.models import SystemUser
from apibackendapp.models import Staff, Doctor

# --- Custom Role-Based Permission Classes ---

class IsStaffOrDoctor(permissions.BasePermission):
    """
    Custom permission to allow read access to any authenticated user,
    but write/edit access (POST, PUT, DELETE) only to users assigned 
    to a 'Staff' or 'Doctor' role via the SystemUser model.
    """
    message = 'You do not have the required medical staff permissions to perform this action.'

    def has_permission(self, request, view):
        # 1. Allow read-only access (GET, HEAD, OPTIONS) for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # 2. Check for write permissions (POST, PUT, PATCH, DELETE)
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            # Find the custom SystemUser object associated with the Django User
            # We assume a one-to-one or one-to-many relationship exists/can be checked.
            # NOTE: If your Staff/Doctor models link directly to the User, 
            # you might need to adjust this lookup (see alternative below).
            
            # --- Primary Lookup (Assuming SystemUser links directly to User or is the primary account type) ---
            system_user = SystemUser.objects.get(username=request.user.username)
            role_name = system_user.role.role_name.lower()
            
            # Allow access if the role is 'Admin', 'Staff', 'Pharmacist', or 'Doctor'
            return role_name in ['admin', 'staff', 'pharmacist', 'doctor']

        except SystemUser.DoesNotExist:
            # If the user is authenticated but has no SystemUser profile, deny write access.
            return False


class IsAdminOrDoctor(permissions.BasePermission):
    """
    Permission for highly sensitive actions (e.g., creating new users/doctors).
    Allows access only to users with 'Admin' or 'Doctor' roles.
    """
    message = 'Access is restricted to Admin and Doctor roles only.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            system_user = SystemUser.objects.get(username=request.user.username)
            role_name = system_user.role.role_name.lower()

            return role_name in ['admin', 'doctor']

        except SystemUser.DoesNotExist:
            return False
            
            
# --- OPTIONAL: Alternative Lookup (If User is linked via Staff/Doctor profile) ---
# If your Staff or Doctor model is the only way a standard User gets a 'role':

class IsStaffOrDoctor_Alt(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if not request.user or not request.user.is_authenticated:
            return False

#         # Check if the user has an associated Staff or Doctor profile
        is_staff_member = Staff.objects.filter(user=request.user).exists()
        is_doctor = Doctor.objects.filter(user=request.user).exists()
        
        return is_staff_member or is_doctor