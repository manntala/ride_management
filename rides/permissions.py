from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsRiderUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "rider"


class IsDriverUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "driver"
