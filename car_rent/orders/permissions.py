from rest_framework import permissions


class BaseAuthUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsOwnerRenterOrder(BaseAuthUserPermission):
    def has_object_permission(self, request, view, obj):
        return (obj.renter == request.user or obj.car.owner == request.user)


class IsCarOwnerOrder(BaseAuthUserPermission):
    def has_object_permission(self, request, view, obj):
        return obj.car.owner == request.user
    

class IsRenterOrder(BaseAuthUserPermission):
    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user
