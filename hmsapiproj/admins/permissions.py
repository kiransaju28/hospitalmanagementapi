from rest_framework import permissions

# --- Helper Permissions ---
# These check the User Group membership

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is in 'Admin' group or is a superuser
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists()
        )

class IsDoctorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Doctor').exists()

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Staff').exists()

# --- ViewSet-Specific Permissions ---

class AdminOnlyPermissions(permissions.BasePermission):
    """
    Allows access only to 'Admin' users or Superusers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists()
        )

class StaffManagementPermissions(permissions.BasePermission):
    """
    - GET (list/retrieve): Admin or Staff
    - POST, PUT, DELETE: Admin only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
        is_staff = request.user.groups.filter(name='Staff').exists()

        # Allow 'Admin' or 'Staff' to view
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return is_admin or is_staff
        
        # Only 'Admin' can create, update, or delete
        return is_admin

class DoctorSelfViewPermissions(permissions.BasePermission):
    """
    - Admin: Full access
    - Staff: Read-only access
    - Doctor: Can view/edit *their own* profile, but not others.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is the Doctor instance
        is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
        is_staff = request.user.groups.filter(name='Staff').exists()
        is_doctor = request.user.groups.filter(name='Doctor').exists()
        
        # Admin has full control
        if is_admin:
            return True

        # Staff can view any doctor profile
        if request.method in permissions.SAFE_METHODS and is_staff:
            return True
        
        # A doctor can view or update their *own* profile
        if is_doctor:
            return obj.user == request.user

        return False