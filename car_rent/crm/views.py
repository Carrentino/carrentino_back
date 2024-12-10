from rest_framework import mixins, viewsets

from cars.models import Car
from cars.serializers.model_serializers import CarSerializer
from crm.permissions import CompanyPermission
from crm.serializers import CarMetricsSerializer
from orders.models import Order
from orders.serializers import OrderSerializer


class CompanyCarView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        return Car.objects.filter(owner__company=self.request.user.company)


class CompanyOrderView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        return Order.objects.filter(car__owner__company=self.request.user.company)

class CarMetricsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarMetricsSerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        return Car.objects.filter(owner__company=self.request.user.company)
