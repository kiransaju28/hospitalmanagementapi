from rest_framework import permissions

class IsDoctorUser(permissions.BasePermission):
    """
    Allows access only to authenticated users in the 'Doctor' group.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Doctor').exists()