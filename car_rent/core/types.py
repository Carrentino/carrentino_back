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
