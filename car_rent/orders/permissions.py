from rest_framework import permissions


class IsOwnerOrderRetrieve(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.renter == request.user or obj.car.owner == request.user)
