from rest_framework.permissions import BasePermission


class CompanyPermission(BasePermission):
    """Пермишен для компании"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.company is not None
