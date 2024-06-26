# Generated by Django 5.0.2 on 2024-04-29 21:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_сar_order_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='desired_date',
        ),
        migrations.AddField(
            model_name='order',
            name='desired_finish_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Планируемое время окончания аренда'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='desired_start_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Планируемое время начала аренды'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='finish_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='фактическое время окончания аренды'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_rent_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='фактическое время начала аренды'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('UC', 'На рассмотрении'), ('AD', 'Одобрен'), ('IP', 'Выполняется'), ('CD', 'Отменен'), ('RD', 'Отклонен')], default='UC', max_length=2, verbose_name='Статус'),
        ),
    ]
