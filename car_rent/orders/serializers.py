from rest_framework import serializers

from .models import Order
from cars.serializers.model_serializers import CarSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderRetriveSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('car', 'desired_finish_datetime', 'desired_start_datetime', )


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('desired_finish_datetime', 'desired_start_datetime')


# class OrderAccept
