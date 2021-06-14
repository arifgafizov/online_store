from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField('отчество', max_length=100, blank=True)
    phone_number = models.CharField('номер телефона', max_length=100, blank=True)
    address = models.CharField('адрес', max_length=100, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return str(self.id) + ' ' + self.username


class PreUser(models.Model):
    username = models.CharField(
        'логин',
        max_length=150,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists."
        })
    password = models.CharField('пароль', max_length=128)
    uuid_token = models.CharField('токен', max_length=150, blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    email = models.EmailField('ел. адрес', blank=True)
    middle_name = models.CharField('отчество', max_length=100, blank=True)
    phone_number = models.CharField('номер телефона', max_length=100, blank=True)
    address = models.CharField('адрес', max_length=100, blank=True)
