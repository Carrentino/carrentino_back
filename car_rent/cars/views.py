from core.views import BaseGetView
from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .choices import CAR_STATUS_CHOCIES
from .filtersets import BrandFilterset, CarModelFilterset
from .models import Brand, Car, CarModel
from .serializers.brief_serializers import (BrandBriefSerialzer,
                                            CarModelBriefSerializer)
from .serializers.model_serializers import (BrandSerializer, CarListSerializer,
                                            CarMapSerializer,
                                            CarModelSerializer, CarSerializer)
from .utils import load_foreign_models


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


class CarView(mixins.ListModelMixin, mixins.CreateModelMixin,
              mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Вьюсет для автомобилей'''
    queryset = Car.objects.filter(status=CAR_STATUS_CHOCIES.VERIFIED)
    queryset_only_fields = {
        'list': ('id', 'title', 'price', 'score'),
        'map': ('id', 'latitude', 'longitude'),
    }
    serializer_class = CarSerializer
    serializer_classes = {
        'list': CarListSerializer,
        'map': CarMapSerializer,
    }

    def get_queryset(self):
        view = self.request.GET.get('view', None)
        if self.action == 'list' and view is not None:
            fields = self.queryset_only_fields.get(view, None)
            if fields is not None:
                return self.queryset.only(fields)
        return self.queryset

    def get_serializer_class(self):
        view = self.request.GET.get('view', None)
        if self.action == 'list' and view is not None:
            return self.serializer_classes.get(view, self.serializer_class)
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        photos_data = request.data.pop('photos', [])
        options_data = request.data.pop('options', [])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        car_instance = serializer.instance

        load_foreign_models(photos_data, options_data, car_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        photos_data = request.data.pop('photos', [])
        options_data = request.data.pop('options', [])

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        car_instance = serializer.instance

        car_instance.car_photo.all().delete()
        car_instance.car_option.all().delete()

        load_foreign_models(photos_data, options_data, car_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
