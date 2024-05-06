import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-list', {'brief': True}, ['id', 'title']],
        ['cars:brand-list', {}, ['id', 'title', 'photos', 'description']],
        ['cars:car-model-list', {'brief': True}, ['id', 'title']],
        ['cars:car-model-list', {}, ['title', 'type_of_fuel',
                                     'id', 'brand', 'hp', 'photos', 'fuel_consumption']],
    ]
)
def test_advanced_cars_list(data, user_client, client, car_model_factory, brand_factory):
    url, params, fields = data
    car_model_factory(id=1)
    brand_factory(id=2)
    rev_url = reverse(url)
    for user, code in [
        (user_client, 200),
        (client, 200),
    ]:
        response = user.get(rev_url, data=params)
        assert response.status_code == code
        json_data = response.json()
        assert set(json_data[0].keys()) == set(fields)


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-detail', 2, ['id', 'title', 'photos', 'description']],
        ['cars:car-model-detail', 1, ['title', 'type_of_fuel',
                                      'id', 'brand', 'hp', 'photos', 'fuel_consumption']],
    ]
)
def test_advanced_cars_retrieve(data, user_client, client, car_model_factory, brand_factory):
    url, pk, fields = data
    car_model_factory(id=pk)
    brand_factory(id=pk)
    rev_url = reverse(url, args=[pk])
    for user, code in [
        (user_client, 200),
        (client, 200),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code
        json_data = response.json()
        assert set(json_data.keys()) == set(fields)
