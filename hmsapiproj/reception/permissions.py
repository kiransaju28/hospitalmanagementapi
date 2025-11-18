from rest_framework import permissions

class IsReceptionStaff(permissions.BasePermission):
    """
    Custom permission to only allow users who are authenticated and 
    belong to the 'Reception' Django Group to perform CRUD operations.
    """
    message = 'Access denied. You must be an authenticated member of the Reception staff group.'

    def has_permission(self, request, view):
        # 1. Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # 2. Check if the user is a superuser (who always has full access)
        if request.user.is_superuser:
            return True

        # 3. Check if the user belongs to the 'Reception' group
        #    (You must ensure a Group named 'Reception' is created in the Django Admin)
        return request.user.groups.filter(name='Reception').exists()


class IsDoctorReadOnly(permissions.BasePermission):
    """
    Permission for resources that are read-only for Reception, but might
    be writable by other roles (like a Doctor or Admin).
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests (safe methods)
        return request.method in permissions.SAFE_METHODS