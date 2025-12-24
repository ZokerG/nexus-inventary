from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission check for Admin users only
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsExternoOrReadOnly(permissions.BasePermission):
    """
    Permission that allows external users only read access
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_admin
