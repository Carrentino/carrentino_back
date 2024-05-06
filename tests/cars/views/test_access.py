import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'url',
    [
        'cars:brand-list',
        'cars:car-model-list',
    ]
)
def test_access_cars_list(url, user_client, client):
    rev_url = reverse(url)
    for user, code in [
        (user_client, 200),
        (client, 200),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-detail', 2],
        ['cars:car-model-detail', 1],
    ]
)
def test_access_cars_retrieve(data, user_client, client, car_model_factory, brand_factory):
    url, pk = data
    car_model_factory(id=pk)
    brand_factory(id=pk)
    rev_url = reverse(url, args=[pk])
    for user, code in [
        (user_client, 200),
        (client, 200),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code
