from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField('отчество', max_length=100)
    phone_number = models.CharField('номер телефона', max_length=100)
    address = models.CharField('адрес', max_length=100)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.last_name + ' ' + self.first_name