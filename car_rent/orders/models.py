from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import BaseAbstractModel
from users.models import User
from cars.models import Car
from .choices import ORDER_STATUSES


class Order(BaseAbstractModel):
    """Model of order"""
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE,
        verbose_name="Арендованный автомобиль",
    )
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Арендатор"
    )
    #  TODO: связь с чатом

    desired_finish_datetime = models.DateTimeField(
        verbose_name="Планируемое время окончания аренда"
    )
    desired_start_datetime = models.DateTimeField(
        verbose_name="Планируемое время начала аренды"
    )
    start_rent_time = models.DateTimeField(
        verbose_name="фактическое время начала аренды",
        null=True, blank=True
    )
    finish_datetime = models.DateTimeField(
        verbose_name="фактическое время окончания аренды",
        null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=2,
        choices=ORDER_STATUSES,
        default=ORDER_STATUSES.UNDER_CONSIDERATION,
    )
    is_renter_start_order = models.BooleanField(
        blank=True, default=False,
        verbose_name="Подтвердил ли арендатор старт заказа"

    )
    is_lessor_start_order = models.BooleanField(
        blank=True, default=False,
        verbose_name="Подтвердил ли арендодатель старт заказа"
    )

    def clean(self) -> None:
        super().clean()
        if self.desired_start_datetime >= self.desired_finish_datetime:
            raise ValidationError("Планируемое время начала аренды должно быть раньше времени окончания аренды")

    class Meta:
        db_table = 'order_table'
        app_label = 'orders'
        unique_together = ['renter', 'car']
