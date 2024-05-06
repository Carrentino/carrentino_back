import pytest


@pytest.fixture
def brand(brand_factory):
    return brand_factory()


@pytest.fixture
def car_model(car_model_factory):
    return car_model_factory()


@pytest.fixture
def car(car_factory):
    return car_factory()
