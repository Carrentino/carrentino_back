# Generated by Django 5.0.2 on 2024-04-29 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_rename_car_car_car_model_car_status_and_more'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='сar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='cars.car', verbose_name='Арендованный автомобиль'),
        ),
    ]
