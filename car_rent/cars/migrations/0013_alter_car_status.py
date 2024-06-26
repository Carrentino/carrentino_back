# Generated by Django 5.0.2 on 2024-05-02 08:27

import core.types
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0012_alter_car_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='status',
            field=core.types.StatusField(choices=[(100, 'Не проверено'), (200, 'Проверено'), (300, 'Архивировано'), (400, 'Заблокировано')], default=100, validators=[
                                         django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)], verbose_name='Статус'),
        ),
    ]
