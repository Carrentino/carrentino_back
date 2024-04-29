from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrderRetrieve
from .models import Order
from .serializers import OrderSerializer, OrderRetriveSerializer, OrderCreateSerializer


@extend_schema_view(
    list_arendodator_orders=extend_schema(
        description="Список заказов арендодателя с возможностью фильтрации по конкретной машине",
        parameters=[
            OpenApiParameter(name='car_id', type=OpenApiTypes.INT, required=False, location=OpenApiParameter.QUERY,
                             description='id автомобиля для получения заказов по нему')
        ],
        responses={
            200: OrderSerializer
        }
    ),
    list_renter_orders=extend_schema(
        description="Получение списка своих заявок на аренду автомобилей от лица арендателя",
        responses={
            200: OrderSerializer
        }
    ),
    retrieve=extend_schema(
        description="Получение конкретного заказа (с правами доступа либо арендатор заказа либо владелец авто заказа)",
        responses={
            200: OrderRetriveSerializer
        }
    ),
    destroy=extend_schema(
        description="Удаление заявки только "
    ),
    create=extend_schema(
        request=OrderCreateSerializer
    )
)
class OrderViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet,
                   mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Order.objects.select_related('car', 'renter')
    serializer_classes = {
        'retrieve': OrderRetriveSerializer,
        'arendodator_orders': OrderSerializer,
        'list_renter_orders': OrderSerializer,
        'create': OrderCreateSerializer
    }
    permission_classes = {
        'retrieve': [IsOwnerOrderRetrieve]
    }
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permission(self):
        return self.permission_classes.get(self.action, [IsAuthenticated])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.validated_data.get('car')
        if Order.objects.filter(renter=request.user, car_id=car):
            return Response(
                {"error": "Вы уже создали заявку на этот автомобиль"},
                status=status.HTTP_409_CONFLICT
            )
        serializer.save(renter=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def list_arendodator_orders(self, request, car_id=None):
        user = request.user
        serializer = self.get_serializer_class()
        car_id = request.query_params.get('car_id')
        if car_id:
            orders = Order.objects.filter(car__owner=user, car_id=car_id)
        else:
            orders = Order.objects.filter(car__owner=user)
        data = serializer(orders, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_renter_orders(self, request):
        user = request.user
        serializer = self.get_serializer_class()
        orders = Order.objects.filter(renter=user)
        data = serializer(orders, many=True).data
        return Response(data, status=status.HTTP_200_OK)

