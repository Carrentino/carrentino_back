import factory
from django.contrib.auth import get_user_model
from faker import Factory as FakerFactory

faker = FakerFactory.create()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User 

    first_name = factory.Faker("word")
    last_name = factory.Faker("word")
    email = factory.Faker("email")
    score = factory.Faker("pyfloat")
