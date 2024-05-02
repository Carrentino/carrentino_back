from core.models import BaseAbstractModel
from core.types import StatusField
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .choices import (BODY_TYPE_CHOCIES, CAR_STATUS_CHOCIES, DRIVE_CHOICES,
                      FUEL_TYPE_CHOICES, GEARBOX_CHOICES)
from .managers import OrderingManager

User = get_user_model()


class Brand(models.Model):
    '''Model of car Brand'''
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание')

    objects = OrderingManager()

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        indexes = [
            GinIndex(fields=['title',], name='brand_title_gin_idx',
                     opclasses=['gin_trgm_ops'])
        ]

    def __str__(self):
        return f'Brand {self.title}'


class CarModel(models.Model):
    '''Model of car Template'''
    title = models.CharField(max_length=100, verbose_name='Название')
    engine_capacity = models.DecimalField(decimal_places=1, max_digits=3, validators=[
                                          MinValueValidator(0.1)], verbose_name='Объем двигателя', null=True)
    drive = models.CharField(
        max_length=3, choices=DRIVE_CHOICES, blank=False, verbose_name='Привод')
    gearbox = models.CharField(
        max_length=2, choices=GEARBOX_CHOICES, blank=False, verbose_name='Коробка передач')
    body_type = models.CharField(
        max_length=2, choices=BODY_TYPE_CHOCIES, blank=False, verbose_name='Тип кузова')
    type_of_fuel = models.CharField(
        max_length=2, choices=FUEL_TYPE_CHOICES, verbose_name='Тип топлива', blank=False)
    fuel_consumption = models.DecimalField(decimal_places=1, max_digits=3, validators=[
                                           MinValueValidator(0.1)], verbose_name='Расход топлива')
    hp = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='Мощность')
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, verbose_name='Марка')

    objects = OrderingManager()

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели'
        indexes = [
            GinIndex(fields=['title',], name='carmodel_title_gin_idx', opclasses=[
                     'gin_trgm_ops'])
        ]

    def __str__(self):
        return f'{self.title} - {self.hp} л.с.'


class Car(BaseAbstractModel):
    '''Model of User's Car'''
    car_model = models.ForeignKey(
        CarModel, on_delete=models.PROTECT, verbose_name='Модель')
    color = models.CharField(max_length=25, verbose_name='Цвет')
    score = models.DecimalField(default=5.0, decimal_places=2, max_digits=3, validators=[
                                MinValueValidator(0.0), MaxValueValidator(5.01)], verbose_name='Рейтинг')
    price = models.PositiveIntegerField(verbose_name='Цена')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Владелец')
    status = StatusField(choices=CAR_STATUS_CHOCIES,
                         default=CAR_STATUS_CHOCIES.NOT_VERIFIED)
    latitude = models.FloatField(verbose_name='Широта')
    langitude = models.FloatField(verbose_name='Долгота')


class CarOptions(models.Model):
    '''Model of car option'''
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            related_name='car_option')
    option = models.CharField(max_length=200)


class CarModelPhoto(models.Model):
    '''Model of car model photo'''
    photo = models.ImageField(upload_to='car_models', verbose_name='Фото')
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE,
                            verbose_name='Модель машины', related_name='carmodel_photo')

    class Meta:
        verbose_name = 'Фотография модели машины'
        verbose_name_plural = 'Фотографии моделей машины'


class BrandPhoto(models.Model):
    '''Model of brand photo'''
    photo = models.ImageField(upload_to='brands', verbose_name='Фото')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='brand_photo')

    class Meta:
        verbose_name = 'Фотография бренда'
        verbose_name_plural = 'Фотографии брендов'


class CarPhoto(models.Model):
    '''Model of User's car photo'''
    photo = models.ImageField(upload_to='cars', verbose_name='Фото')
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            verbose_name='Автомобиль', related_name='car_photo')

    class Meta:
        verbose_name = 'Фотография автомобиля'
        verbose_name_plural = 'Фотографии автомобилей'
