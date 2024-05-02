from rest_framework.permissions import SAFE_METHODS, BasePermission


class CarPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user or request.user.is_superuser or request.method in SAFE_METHODS)
