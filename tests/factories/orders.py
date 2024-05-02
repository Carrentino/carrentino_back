import factory
from orders import models
from faker import Factory as FakerFactory

from .users import UserFactory

faker = FakerFactory.create()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model