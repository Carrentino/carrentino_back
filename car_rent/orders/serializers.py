import datetime
from rest_framework import serializers, status

from .models import Order
from cars.serializers.model_serializers import CarSerializer


class BaseOrderUpdsteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['desired_start_datetime'] >= attrs['desired_finish_datetime']:
            raise serializers.ValidationError("Планируемое время начала аренды должно быть раньше времени окончания аренды")
        return attrs


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderRetriveSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(BaseOrderUpdsteSerializer):
    class Meta:
        model = Order
        fields = ('car', 'desired_finish_datetime', 'desired_start_datetime', )


class OrderUpdateSerializer(BaseOrderUpdsteSerializer):
    class Meta:
        model = Order
        fields = ('desired_finish_datetime', 'desired_start_datetime')



# class OrderAccept
