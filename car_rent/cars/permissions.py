from rest_framework.permissions import SAFE_METHODS, BasePermission


class CarPermission(BasePermission):
    '''Пермишен для автомобиля'''

    def has_object_permission(self, request, view, obj):
        return ((request.user and obj.owner == request.user) or request.method in SAFE_METHODS)


class CarActionPermission(BasePermission):
    '''Пермишен для добавления связаных объектов для автомобиля'''

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and (obj.owner == request.user or request.method in SAFE_METHODS))


class CarForeignPermission(BasePermission):
    '''Пермишен для связных моделей автомобиля'''

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.car.owner == request.user)
