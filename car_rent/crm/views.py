from rest_framework import mixins, viewsets

from cars.models import Car
from cars.serializers.model_serializers import CarSerializer
from crm.permissions import CompanyPermission


class CompanyCarView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        return Car.objects.filter(owner__company=self.request.user.company)
