from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from datetime import timedelta

import pytest

from orders import models
from tests.factories.orders import OrderFactory
from tests.factories.cars import CarFactory
from tests.factories.users import UserFactory
from car_rent.cars.choices import CAR_STATUS_CHOCIES


def test_list_lessor_orders(user_client, user):
    other_user = UserFactory()
    other_user_car = CarFactory(owner=other_user)
    other_user_orders = OrderFactory.create_batch(2, car=other_user_car)
    current_user_car = CarFactory(owner=user)
    current_user_orders = OrderFactory.create_batch(3, car=current_user_car)
    response = user_client.get(reverse("orders:order-list-lessor-orders"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(current_user_orders)


def test_renter_orders(user_client, user):
    other_users_orders = OrderFactory.create_batch(2)
    current_user_orders = OrderFactory.create_batch(3, renter=user)
    response = user_client.get(reverse("orders:order-list-renter-orders"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(current_user_orders)


@pytest.mark.parametrize(
        "url, current_status, response_status", [
            ("orders:order-accept-order", models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_200_OK),
            ("orders:order-accept-order", models.Order.OrderStatus.ACCEPTED, status.HTTP_409_CONFLICT),
            ("orders:order-accept-order", models.Order.OrderStatus.IN_PROGRESS, status.HTTP_409_CONFLICT),
            ("orders:order-accept-order", models.Order.OrderStatus.CANCELED, status.HTTP_409_CONFLICT),
            ("orders:order-accept-order", models.Order.OrderStatus.REJECTED, status.HTTP_409_CONFLICT),
            ("orders:order-accept-order", models.Order.OrderStatus.FINISHED, status.HTTP_409_CONFLICT),

            ("orders:order-reject-order", models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_200_OK),
            ("orders:order-reject-order", models.Order.OrderStatus.ACCEPTED, status.HTTP_409_CONFLICT),
            ("orders:order-reject-order", models.Order.OrderStatus.IN_PROGRESS, status.HTTP_409_CONFLICT),
            ("orders:order-reject-order", models.Order.OrderStatus.CANCELED, status.HTTP_409_CONFLICT),
            ("orders:order-reject-order", models.Order.OrderStatus.REJECTED, status.HTTP_409_CONFLICT),
            ("orders:order-reject-order", models.Order.OrderStatus.FINISHED, status.HTTP_409_CONFLICT),
        ]
)
def test_owner_accept_reject_order(user_client, user, url, current_status, response_status):
    car = CarFactory(owner=user)
    order = OrderFactory(set_status=current_status, car=car)
    response = user_client.post(reverse(url, kwargs={'pk': order.id}))
    if response_status == status.HTTP_200_OK and url == "orders:order-accept-order":
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.status == models.Order.OrderStatus.ACCEPTED
    if response_status == status.HTTP_200_OK and url == "orders:order-reject-order":
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.status == models.Order.OrderStatus.REJECTED
    assert response.status_code == response_status


@pytest.mark.parametrize(
        "current_status, response_status", [
            (models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_200_OK),
            (models.Order.OrderStatus.ACCEPTED, status.HTTP_409_CONFLICT),
            (models.Order.OrderStatus.IN_PROGRESS, status.HTTP_409_CONFLICT),
            (models.Order.OrderStatus.CANCELED, status.HTTP_409_CONFLICT),
            (models.Order.OrderStatus.REJECTED, status.HTTP_409_CONFLICT),
            (models.Order.OrderStatus.FINISHED, status.HTTP_409_CONFLICT),
        ]
)
def test_renter_cancel_order(user_client, user, current_status, response_status):
    order = OrderFactory(set_status=current_status, renter=user)
    response = user_client.post(reverse("orders:order-cancel-order", kwargs={'pk': order.id}))
    if response_status == status.HTTP_200_OK:
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.status == models.Order.OrderStatus.CANCELED
    assert response.status_code == response_status


@pytest.mark.parametrize(
        "current_status, response_status, is_renter_start_order", [
            (models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.ACCEPTED, status.HTTP_200_OK, True),
            (models.Order.OrderStatus.IN_PROGRESS, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.CANCELED, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.REJECTED, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.FINISHED, status.HTTP_409_CONFLICT, False),
        ]
)
def test_lessor_start_rent(user_client, user, current_status, response_status, is_renter_start_order):
    car = CarFactory(owner=user)
    renter = UserFactory()
    order = OrderFactory(car=car, renter=renter, status=current_status, set_is_renter_start_order=is_renter_start_order)
    response = user_client.post(reverse("orders:order-start-rent", kwargs={'pk': order.id}))
    if response_status == status.HTTP_200_OK:
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.is_lessor_start_order is True
        assert refresh_order.status == models.Order.OrderStatus.IN_PROGRESS
    assert response.status_code == response_status


@pytest.mark.parametrize(
        "current_status, response_status, is_lessor_start_order", [
            (models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.ACCEPTED, status.HTTP_200_OK, True),
            (models.Order.OrderStatus.IN_PROGRESS, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.CANCELED, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.REJECTED, status.HTTP_409_CONFLICT, False),
            (models.Order.OrderStatus.FINISHED, status.HTTP_409_CONFLICT, False),
        ]
)
def test_renter_start_rent(user_client, user, current_status, response_status, is_lessor_start_order):
    owner = UserFactory()
    car = CarFactory(owner=owner)
    order = OrderFactory(car=car, renter=user, status=current_status, set_is_lessor_start_order=is_lessor_start_order)
    response = user_client.post(reverse("orders:order-start-rent", kwargs={'pk': order.id}))
    if response_status == status.HTTP_200_OK:
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.is_renter_start_order is True
        assert refresh_order.status == models.Order.OrderStatus.IN_PROGRESS
    assert response.status_code == response_status


@pytest.mark.parametrize(
        "current_status, response_status", [
            (models.Order.OrderStatus.UNDER_CONSIDERATION, status.HTTP_200_OK),
            (models.Order.OrderStatus.ACCEPTED, status.HTTP_403_FORBIDDEN),
            (models.Order.OrderStatus.IN_PROGRESS, status.HTTP_403_FORBIDDEN),
            (models.Order.OrderStatus.CANCELED, status.HTTP_403_FORBIDDEN),
            (models.Order.OrderStatus.REJECTED, status.HTTP_403_FORBIDDEN),
            (models.Order.OrderStatus.FINISHED, status.HTTP_403_FORBIDDEN),
        ]
)
def test_put_update_order_after_consideration(user_client, user, current_status, response_status):
    order = OrderFactory(renter=user, set_status=current_status)
    new_desired_finish_datetime = timezone.now()
    data_to_send = {
        "desired_finish_datetime": new_desired_finish_datetime
    }
    response_put = user_client.put(reverse("orders:order-detail", kwargs={'pk': order.id}), data=data_to_send)
    if response_status == status.HTTP_200_OK:
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.desired_finish_datetime == new_desired_finish_datetime
    new_desired_finish_datetime = timezone.now()
    data_to_send = {
        "desired_finish_datetime": new_desired_finish_datetime
    }
    response_patch = user_client.patch(reverse("orders:order-detail", kwargs={'pk': order.id}), data=data_to_send)
    if response_status == status.HTTP_200_OK:
        refresh_order = models.Order.objects.get(id=order.id)
        assert refresh_order.desired_finish_datetime == new_desired_finish_datetime
    assert response_put.status_code == response_status
    assert response_patch.status_code == response_status
