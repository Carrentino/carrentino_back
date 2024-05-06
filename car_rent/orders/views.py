from django.core.exceptions import ValidationError

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
from .choices import ORDER_STATUSES


@extend_schema_view(
    list_lessor_orders=extend_schema(
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
                    "error": 'Планируемое время начала аренды должно быть раньше времени окончания аренды',
                }
            }
        }
    ),
    partial_update=extend_schema(
        description="Обновление данных заявки",
        request=OrderUpdateSerializer,
        responses={
            status.HTTP_200_OK: OrderUpdateSerializer,
            status.HTTP_409_CONFLICT: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "error": 'Планируемое время начала аренды должно быть раньше времени окончания аренды',
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
                    "error": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
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
                    "error": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
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
                    "error": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
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
            status.HTTP_400_BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                },
                "example": {
                    "error": 'Для изменения на статус <requested_status>, заявка должна находиться в статусе <expected_status>',
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
        'update': OrderUpdateSerializer,
        'partial_update': OrderUpdateSerializer
    }
    permissions_classes = {
        'retrieve': [IsOwnerRenterOrder],
        'update': [IsRenterOrder],
        'partial_update': [IsRenterOrder],
        'accept_order': [IsCarOwnerOrder],
        'reject_order': [IsCarOwnerOrder],
        'cancel_order': [IsRenterOrder],
        'start_rent': [IsOwnerRenterOrder]
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        permissions = self.permissions_classes.get(self.action, [IsAuthenticated])
        return [permission() for permission in permissions]

    def create(self, request, *args, **kwargs):
        """Создание заказа"""
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.validated_data.get('car')
        if Order.objects.filter(renter=request.user, car_id=car).exists():
            return Response(
                {"error": "Вы уже создали заявку на этот автомобиль"},
                status=status.HTTP_409_CONFLICT
            )
        serializer.save(renter=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status != ORDER_STATUSES.UNDER_CONSIDERATION:
            return Response({"error": "нельзя изменить заявку после ее одобрения"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer_class()
        serializer = serializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        desired_finish_datetime = serializer.validated_data.get("desired_finish_datetime", order.desired_finish_datetime)
        desired_start_datetime = serializer.validated_data.get("desired_start_datetime", order.desired_start_datetime)
        if desired_start_datetime >= desired_finish_datetime:
            return Response(
                {"error": "Планируемое время начала аренды должно быть раньше времени окончания аренды"},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        status_checker = check_order_status(order, ORDER_STATUSES.UNDER_CONSIDERATION, ORDER_STATUSES.ACCEPTED)
        if status_checker.get("response"):
            return status_checker["response"]
        order.status = ORDER_STATUSES.ACCEPTED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ подтвержден"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_order(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, ORDER_STATUSES.UNDER_CONSIDERATION, ORDER_STATUSES.REJECTED)
        if status_checker.get("response"):
            return status_checker["response"]
        order.status = ORDER_STATUSES.REJECTED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ отклонен"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, ORDER_STATUSES.UNDER_CONSIDERATION, ORDER_STATUSES.CANCELED)
        # TODO: рарешать ли отмену заказа после одобрения 
        if status_checker.get("response"):
            return status_checker["response"]
        order.status = ORDER_STATUSES.CANCELED
        # TODO: добавить таску для отправки уведов
        order.save()
        return Response({"ok": "Заказ отменен"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def start_rent(self, request, pk=None):
        order = self.get_object()
        status_checker = check_order_status(order, ORDER_STATUSES.ACCEPTED, ORDER_STATUSES.IN_PROGRESS)
        if status_checker.get("response"):
            return status_checker["response"]
        if request.user == order.renter:
            order.is_renter_start_order = True
        else:
            order.is_lessor_start_order = True
        if order.is_lessor_start_order and order.is_renter_start_order:
            order.status = ORDER_STATUSES.IN_PROGRESS
        order.save()
        # TODO: добавить уведы
        # TODO: Попиздеть с егором за ответы
        return Response({"ok": "вы подтвердили старт заказа"}, status=status.HTTP_200_OK)
