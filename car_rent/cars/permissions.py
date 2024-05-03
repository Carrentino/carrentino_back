from rest_framework.permissions import SAFE_METHODS, BasePermission


class CarPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'post':
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return (obj.owner == request.user or request.method in SAFE_METHODS)
