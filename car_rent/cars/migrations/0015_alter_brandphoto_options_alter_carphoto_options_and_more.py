# Generated by Django 5.0.2 on 2024-05-02 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0014_alter_car_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brandphoto',
            options={'verbose_name': 'Фотография бренда',
                     'verbose_name_plural': 'Фотографии брендов'},
        ),
        migrations.AlterModelOptions(
            name='carphoto',
            options={'verbose_name': 'Фотография автомобиля',
                     'verbose_name_plural': 'Фотографии автомобилей'},
        ),
        migrations.AlterField(
            model_name='caroptions',
            name='car',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='car_option', to='cars.car'),
        ),
        migrations.AlterField(
            model_name='carphoto',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='car_photo', to='cars.car', verbose_name='Автомобиль'),
        ),
        migrations.AlterField(
            model_name='carphoto',
            name='photo',
            field=models.ImageField(upload_to='cars', verbose_name='Фото'),
        ),
    ]
