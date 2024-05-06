import pytest
from cars import models
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    'url',
    [
        'cars:brand-list',
        'cars:car-model-list',
    ]
)
def test_access_cars_list(url, user_client, client):
    '''Тест доступа к list эндпоинтов cars'''
    rev_url = reverse(url)
    for user, code in [
        (client, status.HTTP_200_OK),
        (user_client, status.HTTP_200_OK),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code


@pytest.mark.parametrize(
    'data',
    [
        ['cars:brand-detail', 'brand'],
        ['cars:car-model-detail', 'car_model'],
        ['cars:car-detail', 'car'],
    ]
)
def test_access_cars_retrieve(data, request, user_client, client):
    '''Тест доступа к retrieve эндпоинтов cars'''
    url, obj_fixture = data
    obj = request.getfixturevalue(obj_fixture)
    attr = 'pk'
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_200_OK),
        (user_client, status.HTTP_200_OK),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code


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
            [
                {
                    'car_model_factory': {
                        'pk': 1,
                    }
                },
            ],
            models.Car
        ],
    ]
)
def test_access_cars_create(data, user_client, client, run_common_fixtures):
    '''Тест доступа к create эндпоинтов cars'''
    url, req, fixtures, model = data[:4]
    if len(data) > 4:
        attr = data[4]
        rev_url = reverse(url, args=[attr])
    else:
        rev_url = reverse(url)
    run_common_fixtures(fixtures)
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_201_CREATED),
    ]:
        response = user.post(rev_url, data=req)
        assert response.status_code == code
        if response.status_code == status.HTTP_201_CREATED:
            model.objects.filter(id=response.data.get('id')).delete()


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-detail',
            {
                'color': 'white',
            },
            'car',
        ],
    ]
)
def test_access_cars_update(data, request, user_client, client):
    '''Тест доступа к update эндпоинтов cars'''
    url, req, obj_fixture = data
    obj = request.getfixturevalue(obj_fixture)
    attr = 'pk'

    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, 200),
        (user_client, 200),
    ]:
        response = user.get(rev_url)
        print(response.json())
        assert response.status_code == code


# @pytest.mark.parametrize(
#     'data',
#     [
#         ['cars:brand-detail', 3],
#         ['cars:car-model-detail', 2],
#         ['cars:car-detail', 1],
#     ]
# )
# def test_access_cars_delete(data, user_client, client, car_model_factory, brand_factory, car_factory):
#     '''Тест доступа к delete эндпоинтов cars'''
#     url, pk = data
#     car_factory(id=pk)
#     car_model_factory(id=pk)
#     brand_factory(id=pk)
#     rev_url = reverse(url, args=[pk])
#     for user, code in [
#         (user_client, 200),
#         (client, 200),
#     ]:
#         response = user.get(rev_url)
#         print(response.json())
#         assert response.status_code == code
