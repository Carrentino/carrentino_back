# Generated by Django 5.0.2 on 2024-04-29 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_сar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='сar',
            new_name='car',
        ),
    ]
