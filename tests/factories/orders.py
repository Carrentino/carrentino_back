from django.utils import timezone

import factory
from faker import Factory as FakerFactory

from orders import models
from .users import UserFactory
from .cars import CarFactory

faker = FakerFactory.create()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order
    car = factory.SubFactory(CarFactory)
    renter = factory.SubFactory(UserFactory)
    desired_finish_datetime = factory.LazyFunction(timezone.now)
    desired_start_datetime = factory.LazyFunction(timezone.now)
    start_rent_time = factory.LazyFunction(timezone.now)
    finish_datetime = factory.LazyFunction(timezone.now)
    status = factory.Faker('random_element', elements=[choice[0] for choice in models.ORDER_STATUSES])
    is_renter_start_order = factory.Faker('boolean')
    is_lessor_start_order = factory.Faker('boolean')

    @factory.post_generation
    def set_status(self, create, extracted, **kwargs):
        if extracted:
            self.status = extracted
    
    @factory.post_generation
    def set_is_lessor_start_order(self, create, extracted, **kwargs):
        if extracted:
            self.is_lessor_start_order = extracted

    @factory.post_generation
    def set_is_renter_start_order(self, create, extracted, **kwargs):
        if extracted:
            self.is_renter_start_order = extracted