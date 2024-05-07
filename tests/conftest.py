from unittest.mock import MagicMock

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from .factories import cars

User = get_user_model()

register(cars.BrandFactory)
register(cars.CarModelFactory)
register(cars.CarFactory)
register(cars.CarOptionFactory)
register(cars.CarPhotoFactory)


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username='user_client', password='password', email='client@user.ru')
    user.refresh_from_db()
    return user


@pytest.fixture
def user_client(db, user):
    '''Client of registered user'''
    client_instance = APIClient()
    access_token = AccessToken.for_user(user)
    client_instance.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client_instance


@pytest.fixture
def misha(db):
    user = User.objects.create_user(
        username='misha', password='password', email='misha@user.ru')
    user.refresh_from_db()
    return user


@pytest.fixture
def misha_client(db, misha):
    '''Client of registered user'''
    client_instance = APIClient()
    access_token = AccessToken.for_user(misha)
    client_instance.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client_instance


@pytest.fixture
def oleg(db):
    user = User.objects.create_user(
        username='oleg', password='password', email='oleg@user.ru')
    user.refresh_from_db()
    return user


@pytest.fixture
def oleg_client(db, oleg):
    '''Client of registered user'''
    client_instance = APIClient()
    access_token = AccessToken.for_user(oleg)
    client_instance.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
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
    client_instance = APIClient()
    return client_instance


@pytest.fixture
def banned_user(db):
    """Забаненный пользователь"""
    user = User.objects.create_user(
        username='unauthorized_client', password='password', email='unauthorized_client@user.ru', status=User.UserStatus.BANNED)
    return user


@pytest.fixture
def run_common_fixtures(request):

    def _run_common_fixtures(common_fixtures):
        for item in common_fixtures:
            item_type = type(item)
            if item_type is str:
                request.getfixturevalue(item)
            if item_type is dict:
                key, value = next(iter(item.items()))
                request.getfixturevalue(key)(**value)
    return _run_common_fixtures


@pytest.fixture
def mock_image():
    fake_image = MagicMock(spec=SimpleUploadedFile)
    fake_image.name = 'test_photo.jpg'
    fake_image.content_type = 'image/jpeg'
    fake_image.size = 123
    return fake_image
