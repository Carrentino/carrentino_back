from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.choices import USER_ROLES


class User(AbstractUser):
    '''Model of user'''
    class UserStatus(models.TextChoices):
        NOT_VERIFIED = 'NV', _('Не верифицирован')
        VERIFIED = 'VE', _('Верифицирован')
        SUSPECT = 'SU', _('Подозреваемый')
        BANNED = 'BA', _('Заблокирован')

    first_name = models.CharField(
        max_length=200,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия')
    email = models.EmailField(
        unique=True,
        max_length=200,
        verbose_name='Email')
    score = models.FloatField(default=5.0, verbose_name='Рейтинг')
    status = models.CharField(max_length=2, choices=UserStatus,
                              default=UserStatus.NOT_VERIFIED, verbose_name='Статус')
    role = models.CharField(max_length=2, choices=USER_ROLES, default=USER_ROLES.PERSON, verbose_name="Роль")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
