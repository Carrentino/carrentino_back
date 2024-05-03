from core.views import BaseGetView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .choices import CAR_STATUS_CHOCIES
from .filtersets import BrandFilterset, CarModelFilterset
from .models import Brand, Car, CarModel, CarOption, CarPhoto
from .permissions import CarPermission
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
class CarView(mixins.ListModelMixin, mixins.CreateModelMixin,
              mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Вьюсет для автомобилей'''
    queryset = Car.objects.filter(status=CAR_STATUS_CHOCIES.VERIFIED).select_related(
        'car_model',
        'car_model__brand',
        'owner'
    ).prefetch_related(
        'car_photo',
        'car_option',
        'car_model__carmodel_photo',
        'car_model__brand__brand_photo',
        'car_option')
    queryset_only_fields = {
        'list': ('id', 'car_model__title', 'price', 'score'),
        'map': ('id', 'latitude', 'longitude'),
    }
    serializer_class = CarSerializer
    serializer_classes = {
        # views
        'list': CarListSerializer,
        'map': CarMapSerializer,
        # actions
        'add_photo': CarPhotoSerializer,
        'add_option': CarOptionSerializer,
    }
    # permission_classes = [CarPermission | IsAdminUser]
    permission_classes = {
        'create': [IsAuthenticated, IsAdminUser],
        'update': [CarPermission | IsAdminUser],
        'delete': [CarPermission | IsAdminUser],
        'add_photo': [CarPermission | IsAdminUser],
        'add_option': [CarPermission | IsAdminUser],
    }

    def get_queryset(self):
        '''сюда не лезть без острой необходимости. тут царит гармония'''
        view = self.request.GET.get(
            'view', None)  # Смотрим указан ли параметр отображения
        if self.action == 'list':  # Проверяем запрос на экшн лист, если нет то стандартный кверисет
            # Подтягиваем аргументы из дикта по указанному параметру либо None
            fields = self.queryset_only_fields.get(view, None)
            if fields is not None:  # Если None то такого отображения не сущетсвует
                return self.queryset.only(*fields)  # онлим по аргументам
            else:
                raise NotFound(
                    {'error': 'Такого варианта для view не сущетсвует. Возможные варианты list, map'})
        return self.queryset

    def get_serializer_class(self):
        '''сюда не лезть без острой необходимости. тут царит гармония'''
        view = self.request.GET.get(
            'view', None)  # Смотрим указан ли параметр отображения
        # Проверяем запрос на экшн лист, если нет то стандартный сериалайзер
        if self.action == 'list' and view is not None:
            # ретурним сериалайзер с ключом который указан в параметрах
            return self.serializer_classes.get(view, self.serializer_class)
        serializer = self.serializer_classes.get(
            self.action, None)  # стягиваем сериалайзер по экшну
        # возвращаем сериалайзер по экшну если он не None либо стандартный
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

    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        '''Добавление фото'''
        serializer = CarPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(car_id=pk)
        return Response({'ok': 'Фото добавлено'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_option(self, request, pk=None):
        '''Добавление опции'''
        serializer = CarOptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(car_id=pk)
        return Response({'ok': 'Опция добавлена'}, status=status.HTTP_201_CREATED)


class CarPhotoView(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Удаление фото автомобиля'''
    serializer_class = CarPhotoSerializer
    permission_classes = [CarPermission | IsAdminUser]

    def get_queryset(self):
        return CarPhoto.objects.filter(car__owner=self.request.user)


class CarOptionView(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Удаление опции автомобиля'''
    serializer_class = CarOptionSerializer
    permission_classes = [CarPermission | IsAdminUser]

    def get_queryset(self):
        return CarOption.objects.filter(car__owner=self.request.user)
