from rest_framework import permissions


class IsOwnerRenterOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.renter == request.user or obj.car.owner == request.user)


class IsCarOwnerOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.car.owner == request.user
    

class IsRenterOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user
