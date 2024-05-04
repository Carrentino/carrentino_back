from rest_framework.permissions import SAFE_METHODS, BasePermission


class CarPermission(BasePermission):
    '''Пермишен для автомобиля'''

    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user or request.method in SAFE_METHODS)


class CarActionPermission(BasePermission):
    '''Пермишен для добавления связаных объектов для автомобиля'''

    def has_object_permission(self, request, view, obj):
        return (obj.car.owner == request.user or request.method in SAFE_METHODS)
