import factory
from users import models
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
        first_name = FakerFactory("word")
        last_name = FakerFactory("word")
        email = FakerFactory("email")
        score = FakerFactory("pyfloat")
