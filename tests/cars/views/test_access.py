import pytest
from cars import models
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    'url',
    [
        'cars:brand-list',
        'cars:car-model-list',
        'cars:car-map-view',
        'cars:car-list-view',
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
        [
            'cars:car-user-cars-view',
            'car_factory',
        ],
    ]
)
def test_access_user_cars(data, request, user_client, client, misha_client, misha):
    '''Тест доступа к list эндпоинтов cars'''
    url, obj_fixture = data
    request.getfixturevalue(obj_fixture)(owner=misha)
    rev_url = reverse(url)
    for user, code, count in [
        (client, status.HTTP_401_UNAUTHORIZED, None),
        (user_client, status.HTTP_200_OK, 0),
        (misha_client, status.HTTP_200_OK, 1),
    ]:
        response = user.get(rev_url)
        assert response.status_code == code
        if response.status_code == status.HTTP_200_OK:
            assert len(response.json()) == count


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
    url, req, fixtures, model = data

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
            'cars:car-add-option',
            {
                'option': 'option',
            },
            'car_factory',
            models.CarOption,
        ],
    ]
)
def test_access_option_create(data, request, user_client, client, misha, misha_client):
    '''Тест доступа к create эндпоинтов cars'''
    url, req, obj_fixture, model = data
    attr = 'pk'
    obj = request.getfixturevalue(obj_fixture)(owner=misha)
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_403_FORBIDDEN),
        (misha_client, status.HTTP_201_CREATED),
    ]:
        response = user.post(rev_url, data=req)
        assert response.status_code == code
        if response.status_code == status.HTTP_201_CREATED:
            model.objects.filter(id=response.data.get('id')).delete()


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-add-photo',
            'car_factory',
            models.CarPhoto,
            'multipart',
        ]
    ]
)
def test_access_photo_create(data, request, mock_image, user_client, client, misha, misha_client):
    '''Тест доступа к create эндпоинтов cars'''
    url, obj_fixture, model, req_format = data
    attr = 'pk'
    req = {
        'photo': mock_image,
    }
    obj = request.getfixturevalue(obj_fixture)(owner=misha)
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_403_FORBIDDEN),
        (misha_client, status.HTTP_201_CREATED),
    ]:
        response = user.post(rev_url, data=req, format=req_format)
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
            'car_factory',
        ],
    ]
)
def test_access_cars_update(data, request, user_client, client, misha, misha_client):
    '''Тест доступа к update эндпоинтов cars'''
    url, req, obj_fixture = data
    obj = request.getfixturevalue(obj_fixture)(owner=misha)
    attr = 'pk'
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_403_FORBIDDEN),
        (misha_client, status.HTTP_200_OK)
    ]:
        response = user.patch(rev_url, data=req)
        assert response.status_code == code


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-detail',
            'car_factory',
        ],
    ]
)
def test_access_cars_delete(data, request, user_client, client, misha, misha_client):
    '''Тест доступа к delete эндпоинтов cars'''
    url, obj_fixture = data
    obj = request.getfixturevalue(obj_fixture)(owner=misha)
    attr = 'pk'
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_403_FORBIDDEN),
        (misha_client, status.HTTP_204_NO_CONTENT),
    ]:
        response = user.delete(rev_url)
        assert response.status_code == code


@pytest.mark.parametrize(
    'data',
    [
        [
            'cars:car-photo-detail',
            'car_photo_factory',
        ],
        [
            'cars:car-option-detail',
            'car_option_factory',
        ]
    ]
)
def test_access_photo_option_delete(data, request, user_client, client, misha, misha_client):
    '''Тест доступа к delete эндпоинтов cars'''
    url, obj_fixture = data
    obj = request.getfixturevalue(obj_fixture)(car__owner=misha)
    attr = 'pk'
    rev_url = reverse(url, args=[getattr(obj, attr)])
    for user, code in [
        (client, status.HTTP_401_UNAUTHORIZED),
        (user_client, status.HTTP_404_NOT_FOUND),
        (misha_client, status.HTTP_204_NO_CONTENT),
    ]:
        response = user.delete(rev_url)
        assert response.status_code == code
