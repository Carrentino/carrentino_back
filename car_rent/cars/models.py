from core.models import BaseAbstractModel
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    class TYPES_OF_FUEL(models.TextChoices):
        '''Choices of fuel type'''
        AI_92 = '92', _('АИ-92')
        AI_95 = '95', _('АИ-95')
        AI_100 = '10', _('АИ-100')
        GAS = 'GS', _('Газ')
        DIESEL = 'DT', _('Дизельное топливо')
        ELECTRO = 'EL', _('Электричество')

    class DRIVE_CHOICES(models.TextChoices):
        '''Choices of drive'''
        RWD = 'RWD', _('Задний привод')
        FWD = 'FWD', _('Передний привод')
        AWD = 'AWD', _('Полный привод')

    class GEARBOX_CHOICES(models.TextChoices):
        '''Choices of gearbox'''
        MANUAL = 'MA', _('Механическая')
        AUTOMATIC = 'AU', _('Автоматическая')
        ROBOT = 'AR', _('Робот')
        CVT = 'AC', _('Вариатор')

    class BODY_TYPE_CHOCIES(models.TextChoices):
        '''Choices of body type'''
        SEDAN = 'SE', _('Седан')
        LIFTBACK = 'LF', _('Лифтбек')
        COUPE = 'CP', _('Купе')
        HATCHBACK_3 = 'H3', _('Хэтчбек 3 дв.')
        HATCHBACK_5 = 'H5', _('Хэтчбек 5 дв.')
        STATION_WAGON = 'SW', _('Универсал')
        SUV_3 = 'S3', _('Внедорожник 3 дв.')
        SUV_5 = 'S5', _('Внедорожник 5 дв.')
        MINIVAN = 'MV', _('Минивен')
        PICKUP = 'PC', _('Пикап')
        LIMOUSINE = 'LM', _('Лимузин')
        VAN = 'VN', _('Фургон')
        CABRIOLET = 'CB', _('Кабриолет')

    title = models.CharField(max_length=100, verbose_name='Название')
    engine_capacity = models.DecimalField(decimal_places=1, max_digits=3, validators=[
                                          MinValueValidator(0.1)], verbose_name='Объем двигателя')
    drive = models.CharField(
        max_length=3, choices=DRIVE_CHOICES, blank=False, verbose_name='Привод')
    gearbox = models.CharField(
        max_length=2, choices=GEARBOX_CHOICES, blank=False, verbose_name='Коробка передач')
    body_type = models.CharField(
        max_length=2, choices=BODY_TYPE_CHOCIES, blank=False, verbose_name='Тип кузова')
    type_of_fuel = models.CharField(
        max_length=2, choices=TYPES_OF_FUEL, verbose_name='Тип топлива', blank=False)
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
    car = models.ForeignKey(
        CarModel, on_delete=models.PROTECT, verbose_name='Модель')
    color = models.CharField(max_length=25, verbose_name='Цвет')
    score = models.DecimalField(default=5.0, decimal_places=2, max_digits=3, validators=[
                                MinValueValidator(0.0), MaxValueValidator(5.01)], verbose_name='Рейтинг')
    price = models.IntegerField(verbose_name='Цена')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Владелец')
    latitude = models.FloatField(verbose_name='Широта')
    langitude = models.FloatField(verbose_name='Долгота')


class CarOptions(models.Model):
    '''Model of car option'''
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
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
        verbose_name_plural = 'Фотографии бренда'


class CarPhoto(models.Model):
    '''Model of User's car photo'''
    photo = models.ImageField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
