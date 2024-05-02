from core.views import BaseGetView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, viewsets

from .choices import CAR_STATUS_CHOCIES
from .filtersets import BrandFilterset, CarModelFilterset
from .models import Brand, Car, CarModel
from .permissions import CarPermission
from .serializers.brief_serializers import (BrandBriefSerialzer,
                                            CarModelBriefSerializer)
from .serializers.model_serializers import (BrandSerializer, CarListSerializer,
                                            CarMapSerializer,
                                            CarModelSerializer, CarSerializer)


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
)
class CarView(mixins.ListModelMixin, mixins.CreateModelMixin,
              mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Вьюсет для автомобилей'''
    queryset = Car.objects.filter(status=CAR_STATUS_CHOCIES.VERIFIED)
    queryset_only_fields = {
        'list': ('id', 'car_model__title', 'price', 'score'),
        'map': ('id', 'latitude', 'langitude'),
    }
    serializer_class = CarSerializer
    serializer_classes = {
        'list': CarListSerializer,
        'map': CarMapSerializer,
    }
    permission_class = CarPermission

    def get_queryset(self):
        view = self.request.GET.get('view', None)
        if self.action == 'list' and view is not None:
            fields = self.queryset_only_fields.get(view, None)
            if fields is not None:
                return self.queryset.only(*fields)
        return self.queryset

    def get_serializer_class(self):
        view = self.request.GET.get('view', None)
        if self.action == 'list' and view is not None:
            return self.serializer_classes.get(view, self.serializer_class)
        return self.serializer_class
