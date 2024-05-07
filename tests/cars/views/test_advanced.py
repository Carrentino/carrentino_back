import pytest
from cars import models
from django.urls import reverse
from rest_framework import status

from car_rent.cars import choices


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-list', {'brief': True}, ['id', 'title'], 'brand'],
        ['cars:brand-list', {}, ['id', 'title', 'photos', 'description'], 'brand'],
        ['cars:car-model-list', {'brief': True}, ['id', 'title'], 'car_model'],
        ['cars:car-model-list', {}, ['title', 'type_of_fuel',
                                     'id', 'brand', 'hp', 'photos', 'fuel_consumption'], 'car_model'],
        ['cars:car-list', {'view': 'map'},
            ['id', 'latitude', 'longitude'], 'car'],
        ['cars:car-list', {'view': 'list'},
            ['price', 'id', 'score', 'car_model'], 'car'],
    ]
)
def test_advanced_cars_list(data, request, user_client, client):
    url, params, fields, obj_fixture = data
    request.getfixturevalue(obj_fixture)
    rev_url = reverse(url)
    for user, code in [
        (user_client, status.HTTP_200_OK),
        (client, status.HTTP_200_OK),
    ]:
        response = user.get(rev_url, data=params)
        assert response.status_code == code
        json_data = response.json()
        assert set(json_data[0].keys()) == set(fields)


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-detail', ['id', 'title', 'photos', 'description'], 'brand'],
        ['cars:car-model-detail', ['title', 'type_of_fuel',
                                   'id', 'brand', 'hp', 'photos', 'fuel_consumption'], 'car_model'],
        ['cars:car-detail', ['car_model', 'latitude', 'status', 'options',
                             'score', 'color', 'id', 'longitude', 'photos', 'price', 'owner'], 'car']
    ]
)
def test_advanced_cars_retrieve(data, request, user_client, client):
    url, fields, obj_fixture = data
    attr = 'pk'
    obj = request.getfixturevalue(obj_fixture)
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (user_client, status.HTTP_200_OK),
        (client, status.HTTP_200_OK),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code
        json_data = response.json()
        assert set(json_data.keys()) == set(fields)


@pytest.mark.parametrize(
    'data',
    [
        ['cars:car-list', ['price', 'color', 'longitude', 'latitude', 'car_model_id']]
    ]
)
def test_advanced_cars_create(data, request, user_client):
    url, fields = data
    rev_url = reverse(url)
    response = user_client.post(rev_url)
    json_data = response.json()
    assert set(json_data.keys()) == set(fields)


@pytest.mark.parametrize(
    'data',
    [
        ['cars:car-add-photo', ['photo',], 'car_factory'],
        ['cars:car-add-option', ['option',], 'car_factory'],
    ]
)
def test_advanced_option_photo_create(data, request, misha, misha_client):
    url, fields, obj_fixture = data
    attr = 'pk'
    obj = request.getfixturevalue(obj_fixture)(owner=misha)
    rev_url = reverse(url, args=[getattr(obj, attr)])
    response = misha_client.post(rev_url)
    json_data = response.json()
    assert set(json_data.keys()) == set(fields)


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-list',
            {
                'car_model_id': 1,
                'color': 'black',
                'price': 2000,
                'latitude': 1.1,
                'longitude': 1.1,
            },

            models.Car
        ],
    ]
)
def test_advanced_car_autofields_create(data, user_client, car_model_factory):
    '''Тест доступа к create эндпоинтов cars'''
    url, req, model = data[:4]
    rev_url = reverse(url)
    car_model_factory(pk=1)
    response = user_client.post(rev_url, data=req)
    assert response.status_code == status.HTTP_201_CREATED
    json_resp = response.json()
    assert json_resp['status'] == choices.CAR_STATUS_CHOICES.NOT_VERIFIED
    assert json_resp['score'] == '5.00'
    if response.status_code == status.HTTP_201_CREATED:
        model.objects.filter(id=response.data.get('id')).delete()


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-list',
            {
                'car_model_id': 1,
                'color': 'black',
                'price': -2000,
                'latitude': 1.1,
                'longitude': 1.1,
            },

            models.Car
        ],
    ]
)
def test_advanced_car_validators_create(data, user_client, car_model_factory):
    '''Тест доступа к create эндпоинтов cars'''
    url, req, model = data[:4]
    rev_url = reverse(url)
    car_model_factory(pk=1)
    response = user_client.post(rev_url, data=req)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_resp = response.json()
    assert json_resp['price'] == [
        'Ensure this value is greater than or equal to 0.']
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        model.objects.filter(id=response.data.get('id')).delete()
