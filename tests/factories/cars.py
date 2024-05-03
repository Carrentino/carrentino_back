import factory
from cars import models
from faker import Factory as FakerFactory

from .users import UserFactory
from car_rent.cars.choices import CAR_STATUS_CHOCIES

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
    score = factory.Faker('pydecimal', left_digits=1, right_digits=2, positive=True, min_value=1, max_value=5)
    price = factory.Faker("pyint")
    owner = factory.SubFactory(UserFactory)
    status = factory.Faker('random_element', elements=[choice[0] for choice in CAR_STATUS_CHOCIES])
    latitude = factory.Faker('latitude')
    langitude = factory.Faker('longitude')

    @factory.post_generation
    def set_status(self, create, extracted, **kwargs):
        if extracted:
            self.status = extracted
