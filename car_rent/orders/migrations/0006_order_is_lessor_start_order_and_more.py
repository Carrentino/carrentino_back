# Generated by Django 5.0.2 on 2024-05-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_desired_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_lessor_start_order',
            field=models.BooleanField(blank=True, default=False, verbose_name='Подтвердил ли арендодатель старт заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_renter_start_order',
            field=models.BooleanField(blank=True, default=False, verbose_name='Подтвердил ли арендатор старт заказа'),
        ),
    ]