from cars.models import (Brand, BrandPhoto, Car, CarModel, CarModelPhoto,
                         CarOption, CarPhoto)
from rest_framework import serializers
from users.serializers.model_serializers import UserSerializer


class BrandPhotoSerializer(serializers.ModelSerializer):
    '''Сериалайзер фото бренда'''
    class Meta:
        model = BrandPhoto
        fields = [
            'id',
            'photo',
        ]


class BrandSerializer(serializers.ModelSerializer):
    '''Сериалайзер бренда'''
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
    '''Сериалайзер фото модели автомобиля'''
    class Meta:
        model = CarModelPhoto
        fields = [
            'id',
            'photo',
        ]


class CarModelSerializer(serializers.ModelSerializer):
    '''Сериалайзер модели автомобиля'''
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
    '''Сериалайзер фотографии автомобиля'''

    class Meta:
        model = CarPhoto
        fields = [
            'id',
            'photo',
        ]


class CarOptionSerializer(serializers.ModelSerializer):
    '''Сериалайзер опции автомобиля'''
    class Meta:
        model = CarOption
        fields = [
            'id',
            'option',
        ]


class CarSerializer(serializers.ModelSerializer):
    '''Сериалайзер автомобилей'''
    car_model = CarModelSerializer(read_only=True)
    car_model_id = serializers.CharField(write_only=True)

    owner = UserSerializer(read_only=True)
    status = serializers.IntegerField(read_only=True)
    score = serializers.DecimalField(
        decimal_places=2, max_digits=3, read_only=True)

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
            'status',
            'latitude',
            'longitude',
            'photos',
            'options',
        ]


class CarListSerializer(serializers.ModelSerializer):
    '''Сериалайзер отображения автомобилей в списке'''
    class Meta:
        model = Car
        fields = [
            'id',
            'car_model',
            'price',
            'score',
        ]


class CarMapSerializer(serializers.ModelSerializer):
    '''Сериалайзер отображения автомобилей на карте'''
    class Meta:
        model = Car
        fields = [
            'id',
            'latitude',
            'longitude',
        ]
