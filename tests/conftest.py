import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from pytest_factoryboy import register

from .factories import cars

User = get_user_model()

register(cars.BrandFactory)
register(cars.CarModelFactory)


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username='user_client', password='password', email='client@user.ru')
    user.refresh_from_db()
    return user


@pytest.fixture
def user_client(db, user):
    '''Client of registered user'''
    client_instance = Client()
    client_instance.force_login(user)
    return client_instance


@pytest.fixture
def registered_user(db):
    '''Registered user'''
    user = User.objects.create_user(
        username='registered_user', email='test@example.com', password='password123')
    user.refresh_from_db()
    return user


@pytest.fixture
def unauthorized_user(db):
    """Неавторизованный пользователь"""
    user = User.objects.create_user(
        username='unauthorized_client', password='password', email='unauthorized_client@user.ru')
    user.refresh_from_db()
    client_instance = Client()
    return client_instance
