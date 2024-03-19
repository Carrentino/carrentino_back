from django_filters import rest_framework as filters

from .models import Brand, CarModel


class BaseCarsFilterset(filters.FilterSet):
    '''Base fiterset of cars'''
    title = filters.CharFilter(field_name='title', lookup_expr='istartswith')

    class Meta:
        abstract = True
        fields = [
            'title',
        ]

    def filter_title(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(title__istartswith=value)


class BrandFilterset(BaseCarsFilterset):
    '''Filterset for brands'''
    class Meta:
        model = Brand
        fields = [
            'title',
        ]


class CarModelFilterset(BaseCarsFilterset):
    '''Filterset for CarModel'''
    class Meta:
        model = CarModel
        fields = [
            'title',
        ]
