from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Admin permission that returns 403 if user is not autorizated"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_staff:
            raise exceptions.PermissionDenied()
        return True