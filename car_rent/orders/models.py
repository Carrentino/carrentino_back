from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import BaseAbstractModel
from users.models import User
from cars.models import Car


class Order(BaseAbstractModel):
    """Model of order"""
    class OrderStatus(models.TextChoices):
        UNDER_CONSIDERATION = 'UC', _("На рассмотрении")
        ACCEPTED = 'AD', _("Одобрен")
        IN_PROGRESS = 'IP', _("Выполняется")
        CANCELED = 'CD', _("Отменен")
        REJECTED = 'RD', _("Отклонен")
        FINISHED = 'FD', _("Завершен")
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
        choices=OrderStatus.choices,
        default=OrderStatus.UNDER_CONSIDERATION,
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

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValueError("Вы уже создали заявку на этот автомобиль")

    class Meta:
        db_table = 'order_table'
        unique_together = ['renter', 'car']
