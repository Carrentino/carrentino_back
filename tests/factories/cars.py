import factory
from cars import models
from faker import Factory as FakerFactory

from car_rent.cars.choices import CAR_STATUS_CHOICES

from .users import UserFactory

faker = FakerFactory.create()


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    title = factory.LazyFunction(lambda: faker.name())


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CarModel

    title = factory.LazyFunction(lambda: faker.name())
    fuel_consumption = factory.LazyFunction(lambda: faker.random_number(
        digits=1) + faker.random_number(digits=1, fix_len=False) * 0.01)
    hp = factory.LazyFunction(lambda: faker.random_int(min=5, max=15))
    brand = factory.SubFactory(BrandFactory)


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Car
    car_model = factory.SubFactory(CarModelFactory)
    color = factory.Faker('word')
    score = factory.Faker('pydecimal', left_digits=1,
                          right_digits=2, positive=True, min_value=1, max_value=5)
    price = factory.Faker("pyint")
    owner = factory.SubFactory(UserFactory)
    status = CAR_STATUS_CHOICES.VERIFIED
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')

    # @factory.post_generation
    # def set_status(self, create, extracted, **kwargs):
    #     if extracted:
    #         self.status = extracted


class CarOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CarOption

    car = factory.SubFactory(CarFactory)
    option = factory.Faker('word')


class CarPhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CarPhoto
    car = factory.SubFactory(CarFactory)
    photo = factory.django.FileField(name='test_photo.jpg')
