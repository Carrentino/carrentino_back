from .models import CarOptions, CarPhoto


def load_foreign_models(photos_data, options_data, car_instance):
    '''Загрузка связанных моделей для автомобиля'''
    photo_objects = [CarPhoto(car=car_instance, **photo_data)
                     for photo_data in photos_data]
    CarPhoto.objects.bulk_create(photo_objects)

    option_objects = [CarOptions(car=car_instance, **option_data)
                      for option_data in options_data]
    CarOptions.objects.bulk_create(option_objects)
