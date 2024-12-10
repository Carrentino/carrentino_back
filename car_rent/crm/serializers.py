from rest_framework import serializers

from cars.models import Car


class CarMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "wathced",
            "bought",
        ]
