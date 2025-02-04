from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print(f"BYBY: {request.user.is_admin}")
        return request.user.is_admin