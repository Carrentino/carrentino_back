from .models import CarOptions, CarPhoto


def load_foreign_models(photos_data, options_data, car_instance):
    '''Загрузка связанных моделей для автомобиля'''
    for photo_data in photos_data:
        CarPhoto.objects.create(car=car_instance, **photo_data)

    for option_data in options_data:
        CarOptions.objects.create(car=car_instance, **option_data)
