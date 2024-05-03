from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from datetime import timedelta

import pytest

from tests.factories.orders import OrderFactory
from tests.factories.cars import CarFactory
from tests.factories.users import UserFactory
from car_rent.cars.choices import CAR_STATUS_CHOCIES


@pytest.mark.parametrize(
    "url, args", [
        ("orders:order-list", None),
        ("orders:order-detail", {"pk": 1}),
        ("orders:order-list-lessor-orders", None),
        ("orders:order-list-renter-orders", None),
        ("orders:order-accept-order", {'pk': 1}),
        ("orders:order-reject-order", {'pk': 1}),
        ("orders:order-cancel-order", {'pk': 1}),
        ("orders:order-start-rent", {'pk': 1})
    ]
)
def test_access_post_api_orders_by_unauthorized_user(unauthorized_user, url, args):
    response = unauthorized_user.post(reverse(url, args=args), data={})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_other_api_orders_by_unauthorized_user(unauthorized_user):
    response_patch = unauthorized_user.patch(reverse("orders:order-detail", args={'pk': 1}), data={})
    response_put = unauthorized_user.patch(reverse("orders:order-detail", args={'pk': 1}), data={})
    response_list = unauthorized_user.get(reverse("orders:order-list"))
    response_retrieve = unauthorized_user.get(reverse("orders:order-detail", args={"pk": 1}))
    assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_list.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_retrieve.status_code == status.HTTP_401_UNAUTHORIZED


def test_twice_create_order_for_one_car(user_client, user):
    car = CarFactory(status=CAR_STATUS_CHOCIES.VERIFIED)
    order = OrderFactory(car=car, renter=user)
    data_to_send = {
        "car": car.id,
        "desired_start_datetime": timezone.now(),
        "desired_finish_datetime": timezone.now() + timedelta(hours=1)
    }
    response = user_client.post(reverse("orders:order-list"), data=data_to_send)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_order_with_invalid_start_finish_datetime(user_client):
    car = CarFactory(status=CAR_STATUS_CHOCIES.VERIFIED)
    data_to_send = {
        "car": car.id,
        "desired_start_datetime": timezone.now(),
        "desired_finish_datetime": timezone.now() - timedelta(hours=1)
    }
    response = user_client.post(reverse("orders:order-list"), data=data_to_send)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
