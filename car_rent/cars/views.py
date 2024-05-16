from core.views import BaseGetView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .choices import CAR_STATUS_CHOICES
from .filtersets import BrandFilterset, CarModelFilterset
from .models import Brand, Car, CarModel, CarOption, CarPhoto
from .permissions import (CarActionPermission, CarForeignPermission,
                          CarPermission)
from .serializers.brief_serializers import (BrandBriefSerialzer,
                                            CarModelBriefSerializer)
from .serializers.model_serializers import (BrandSerializer, CarListSerializer,
                                            CarMapSerializer,
                                            CarModelSerializer,
                                            CarOptionSerializer,
                                            CarPhotoSerializer, CarSerializer)


@extend_schema_view(
    list=extend_schema(
        description="List brands",
        parameters=[
            OpenApiParameter(name='brief', type=OpenApiTypes.BOOL, required=False, location=OpenApiParameter.QUERY,
                             description='If provided and set to true, returns brief representation of brands')
        ]
    ),
    retrieve=extend_schema(
        description="Retrieve a brands"
    )
)
class BrandView(BaseGetView):
    '''View for brands, only list and retrieve'''
    queryset = Brand.objects.prefetch_related('brand_photo')
    queryset_brief = Brand.objects.only('id', 'title').all()
    serializer_class = BrandSerializer
    serializer_class_brief = BrandBriefSerialzer
    filterset_class = BrandFilterset


@extend_schema_view(
    list=extend_schema(
        description="List car models",
        parameters=[
            OpenApiParameter(name='brief', type=OpenApiTypes.BOOL, required=False, location=OpenApiParameter.QUERY,
                             description='If provided and set to true, returns brief representation of car models.')
        ]
    ),
    retrieve=extend_schema(
        description="Retrieve a car model"
    )
)
class CarModelView(BaseGetView):
    '''View for car models, only list and retrieve'''
    queryset = CarModel.objects.select_related(
        'brand').prefetch_related('carmodel_photo', 'brand__brand_photo')
    queryset_brief = CarModel.objects.only('id', 'title').all()
    serializer_class = CarModelSerializer
    serializer_class_brief = CarModelBriefSerializer
    filterset_class = CarModelFilterset


@extend_schema_view(
    list=extend_schema(
        description="Список автомобилей",
        parameters=[
            OpenApiParameter(name='view', type=OpenApiTypes.STR, required=False, location=OpenApiParameter.QUERY,
                             description='Вид отображения список/карта', enum=['map', 'list'])
        ]
    ),
    map_view=extend_schema(
        request=CarMapSerializer,
        responses={
            status.HTTP_201_CREATED: CarMapSerializer,
        }
    ),
    list_view=extend_schema(
        request=CarListSerializer,
        responses={
            status.HTTP_201_CREATED: CarListSerializer,
        }
    ),
    user_cars_view=extend_schema(
        request=CarListSerializer,
        responses={
            status.HTTP_201_CREATED: CarListSerializer,
            status.HTTP_401_UNAUTHORIZED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        }
    ),
    add_photo=extend_schema(
        request=CarPhotoSerializer,
        responses={
            status.HTTP_201_CREATED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Фото добавлено',
                }
            },
            status.HTTP_401_UNAUTHORIZED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        }
    ),
    add_option=extend_schema(
        request=CarOptionSerializer,
        responses={
            status.HTTP_201_CREATED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Опция добавлена',
                }
            },
            status.HTTP_401_UNAUTHORIZED: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        }
    )
)
class CarView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin, mixins.DestroyModelMixin,
              viewsets.GenericViewSet):
    '''Вьюсет для автомобилей'''
    queryset = Car.objects.all()

    action_querysets = {
        'map_view': queryset.filter(status=CAR_STATUS_CHOICES.VERIFIED),
        'list_view': queryset.filter(status=CAR_STATUS_CHOICES.VERIFIED).select_related('car_model', 'car_model__brand'),
        'user_cars_view': queryset.select_related('car_model', 'car_model__brand'),
    }

    default_queryset = queryset.select_related(
        'car_model',
        'car_model__brand',
        'owner'
    ).prefetch_related(
        'car_photo',
        'car_option',
        'car_model__carmodel_photo',
        'car_model__brand__brand_photo',
    )

    serializer_class = CarSerializer
    serializer_classes = {
        'map_view': CarMapSerializer,
        'list_view': CarListSerializer,
        'user_cars_view': CarListSerializer,
        'add_photo': CarPhotoSerializer,
        'add_option': CarOptionSerializer,
    }

    permission_classes = {
        'create': [IsAuthenticated | IsAdminUser],
        'partial_update': [CarPermission | IsAdminUser],
        'destroy': [CarPermission | IsAdminUser],
        'user_cars_view': [IsAuthenticated],
        'add_photo': [CarActionPermission | IsAdminUser],
        'add_option': [CarActionPermission | IsAdminUser],
    }

    def get_queryset(self):
        queryset = self.action_querysets.get(self.action, None)
        return queryset if queryset is not None else self.default_queryset

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer if serializer is not None else self.serializer_class

    def get_permissions(self):
        permissions = self.permission_classes.get(self.action, [AllowAny,])
        return [permission() for permission in permissions]

    def create(self, request, *args, **kwargs):
        """Создание заказа"""
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get',])
    def map_view(self, request):
        '''Автомобили на карте'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get',])
    def list_view(self, request):
        '''Автомобили списком'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get',])
    def user_cars_view(self, request):
        '''Автомобили пользователя'''
        queryset = self.get_queryset().filter(owner=request.user)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        '''Добавление фото'''
        car = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(car=car)
        return Response({'ok': 'Фото добавлено'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_option(self, request, pk=None):
        '''Добавление опции'''
        car = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(car=car)
        return Response({'ok': 'Опция добавлена'}, status=status.HTTP_201_CREATED)


class CarPhotoView(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Удаление фото автомобиля'''
    serializer_class = CarPhotoSerializer
    permission_classes = [CarForeignPermission | IsAdminUser]

    def get_queryset(self):
        return CarPhoto.objects.filter(car__owner=self.request.user)


class CarOptionView(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Удаление опции автомобиля'''
    serializer_class = CarOptionSerializer
    permission_classes = [CarForeignPermission | IsAdminUser]

    def get_queryset(self):
        return CarOption.objects.filter(car__owner=self.request.user)
