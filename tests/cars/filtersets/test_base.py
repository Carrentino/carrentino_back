import pytest
from cars.filtersets import BrandFilterset, CarModelFilterset
from cars.models import Brand, CarModel


@pytest.mark.parametrize(
    'data',
    [
        [{'title': 'BMW'}, 1],
    ]
)
def test_brands_filterset(db, setup, data):
    params, count = data
    assert BrandFilterset(queryset=Brand.objects.all(),
                          data=params).qs.count() == count


@pytest.mark.parametrize(
    'data',
    [
        [{'title': 'A'}, 1],
    ]
)
def test_carmodels_filterset(db, setup, data):
    params, count = data
    assert CarModelFilterset(
        queryset=CarModel.objects.all(), data=params).qs.count() == count
