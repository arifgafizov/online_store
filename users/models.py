from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField('отчество', max_length=100, blank=True, null=True)
    phone_number = models.CharField('номер телефона', max_length=100, blank=True, null=True)
    address = models.CharField('адрес', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return str(self.id) + ' ' + self.username
