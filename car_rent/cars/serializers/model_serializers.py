from cars.models import (Brand, BrandPhoto, Car, CarModel, CarModelPhoto,
                         CarOptions, CarPhoto)
from rest_framework import serializers
from users.serializers.model_serializers import UserSerializer


class BrandPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandPhoto
        fields = ['photo',]


class BrandSerializer(serializers.ModelSerializer):
    '''Serializer of brands'''
    photos = BrandPhotoSerializer(source='brand_photo', many=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'title',
            'description',
            'photos',
        ]


class CarModelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelPhoto
        fields = ['photo',]


class CarModelSerializer(serializers.ModelSerializer):
    '''Serializer of car models'''
    photos = CarModelPhotoSerializer(source='carmodel_photo', many=True)
    brand = BrandSerializer()

    class Meta:
        model = CarModel
        fields = [
            'id',
            'title',
            'brand',
            'type_of_fuel',
            'fuel_consumption',
            'hp',
            'photos',
        ]


class CarPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarPhoto
        fields = ['photo',]


class CarOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarOptions
        fields = ['option',]


class CarSerializer(serializers.ModelSerializer):
    '''Сериалайзер автомобилей'''
    car_model = CarModelSerializer(read_only=True)
    car_model_id = serializers.CharField(write_only=True)

    owner = UserSerializer(read_only=True)
    owner_id = serializers.CharField(write_only=True)
    status = serializers.IntegerField(read_only=True)

    photos = CarPhotoSerializer(source='car_photo', many=True, read_only=True)
    options = CarOptionSerializer(
        source='car_option', many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'car_model',
            'car_model_id',
            'color',
            'score',
            'price',
            'owner',
            'owner_id',
            'status',
            'latitude',
            'langitude',
            'photos',
            'options',
        ]


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'id',
            'title',
            'price',
            'score',
        ]


class CarMapSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'id',
            'latitude',
            'longitude',
        ]
