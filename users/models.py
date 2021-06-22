from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=True)
    middle_name = models.CharField('отчество', max_length=100, blank=True)
    phone_number = models.CharField('номер телефона', max_length=100, blank=True)
    address = models.CharField('адрес', max_length=100, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return str(self.id) + ' ' + self.username


class PreUser(models.Model):
    username = models.CharField('логин', max_length=150)
    uuid_token = models.CharField('токен', max_length=150, blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    email = models.EmailField('ел. адрес', max_length=150)
    middle_name = models.CharField('отчество', max_length=100, blank=True)
    phone_number = models.CharField('номер телефона', max_length=100, blank=True)
    address = models.CharField('адрес', max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'предварительный пользователь'
        verbose_name_plural = 'предварительные пользователи'
