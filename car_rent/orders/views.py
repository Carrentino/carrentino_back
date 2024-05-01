from django.shortcuts import get_object_or_404

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerRenterOrder, IsCarOwnerOrder, IsRenterOrder
from .models import Order
from .serializers import OrderSerializer, OrderRetriveSerializer, OrderCreateSerializer, OrderUpdateSerializer
from .utils import check_order_status


@extend_schema_view(
    list_arendodator_orders=extend_schema(
        description="Список заказов арендодателя с возможностью фильтрации по конкретной машине",
        parameters=[
            OpenApiParameter(name='car_id', type=OpenApiTypes.INT, required=False, location=OpenApiParameter.QUERY,
                             description='id автомобиля для получения заказов по нему')
        ],
        responses={
            status.HTTP_200_OK: OrderSerializer
        }
    ),
    list_renter_orders=extend_schema(
        description="Получение списка своих заявок на аренду автомобилей от лица арендателя",
        responses={
            status.HTTP_200_OK: OrderSerializer
        }
    ),
    retrieve=extend_schema(
        description="Получение конкретного заказа (с правами доступа либо арендатор заказа либо владелец авто заказа)",
        responses={
            status.HTTP_200_OK: OrderRetriveSerializer
        }
    ),
    create=extend_schema(
        description="Создание заявки на аренду авто",
        request=OrderCreateSerializer,
        responses={
            status.HTTP_200_OK: OrderCreateSerializer,
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "error": 'Вы уже создали заявку на этот автомобиль',
                }
            },
        },
    ),
    update=extend_schema(
        description="Обновление данных заявки",
        responses={
            status.HTTP_200_OK: OrderUpdateSerializer,
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "error": 'финишная дата и время не могут быть меньше стартовойй даты и время',
                }
            }
        }
    ),
    accept_order=extend_schema(
        description="Одобрение заявки арендодателем",
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Заказ подтвержден',
                }
            },
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
                }
            }
        }
    ),
    reject_order=extend_schema(
        description='Отклонение заявки арендодателем',
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Заказ отклонен',
                }
            },
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
                }
            }
        }
    ),
    cancel_order=extend_schema(
        description="Отмена заявки арендатором",
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Заказ отменен',
                }
            },
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
                }
            }
        }
    ),
    start_rent=extend_schema(
        description="Старт аренды",
        responses={
            status.HTTP_200_OK: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'вы подтвердили старт заказа',
                }
            },
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "ok": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
                }
            }
        }
    )
)
class OrderViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet,
                   mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Order.objects.select_related('car', 'renter')
    serializer_classes = {
        'retrieve': OrderRetriveSerializer,
        'list_lessor_orders': OrderSerializer,
        'list_renter_orders': OrderSerializer,
        'create': OrderCreateSerializer,
        'update': OrderUpdateSerializer
    }
    permission_classes = {
        'retrieve': [IsOwnerRenterOrder],
        'accept_order': [IsCarOwnerOrder],
        'reject_order': [IsCarOwnerOrder],
        'cancel_order': [IsRenterOrder],
        'start_rent': [IsOwnerRenterOrder]
    }
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permission(self):
        return self.permission_classes.get(self.action, [IsAuthenticated])
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        finish_datetime = serializer.validated_data.get('desired_finish_datetime')
        start_datetime = serializer.validated_data.get('desired_start_datetime')
        if start_datetime > finish_datetime:
            return Response({"error": "финишная дата и время не могут быть меньше стартовойй даты и время"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Создание заказа"""
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
    def list_lessor_orders(self, request, car_id=None):
        """Поулчение списка заказов на свои/ю машины/у"""
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
        """Получение списка заказов оформленных юзером"""
        user = request.user
        serializer = self.get_serializer_class()
        orders = Order.objects.filter(renter=user)
        data = serializer(orders, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept_order(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, Order.OrderStatus.UNDER_CONSIDERATION, Order.OrderStatus.ACCEPTED)
        if not status_checker[0]:
            return status_checker[1]
        order.status = Order.OrderStatus.ACCEPTED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ подтвержден"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_order(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, Order.OrderStatus.UNDER_CONSIDERATION, Order.OrderStatus.REJECTED)
        if not status_checker[0]:
            return status_checker[1]
        order.status = Order.OrderStatus.REJECTED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ отклонен"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, Order.OrderStatus.UNDER_CONSIDERATION, Order.OrderStatus.CANCELED)
        if not status_checker[0]:
            return status_checker[1]
        order.status = Order.OrderStatus.CANCELED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ отменен"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def start_rent(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, Order.OrderStatus.ACCEPTED, Order.OrderStatus.IN_PROGRESS)
        if not status_checker[0]:
            return status_checker[1]
        if request.user == order.renter:
            order.is_renter_start_order = True
        else:
            order.is_lessor_start_order = True
        if order.is_lessor_start_order and order.is_renter_start_order:
            order.status = Order.OrderStatus.IN_PROGRESS
        order.save()
        # TODO: добавить уведы
        return Response({"ok": "вы подтвердили старт заказа"}, status=status.HTTP_200_OK)
