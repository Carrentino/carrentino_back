from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ChoicesMeta(type):
    def __call__(cls, *args, **kwargs):
        return getattr(cls, 'CHOICES', ())

    def __iter__(cls):
        choices = getattr(cls, 'CHOICES', ())
        return iter(choices)


class Choices(metaclass=ChoicesMeta):
    CHOICES = list()

    @classmethod
    def values(cls):
        return [c[0] for c in cls.CHOICES]

    @classmethod
    def as_dict(cls):
        return dict(cls.CHOICES)


class StatusField(models.PositiveSmallIntegerField):
    '''Choices ключом которого является число от 100 до 999'''

    def __init__(self, choices: Choices, **kwargs):
        kwargs['validators'] = kwargs.get(
            'validators', [MinValueValidator(100), MaxValueValidator(999)])
        default = kwargs.get('default', None)
        if default is None:
            raise ValueError('Default value is required for StatusField')
        kwargs['default'] = default
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'Статус')
        kwargs['choices'] = choices
        super().__init__(**kwargs)
