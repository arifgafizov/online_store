from django.db import models

from common.base_model import BaseModel
from online_store.models_manager import AvailableObjectsManager


class Product(BaseModel):
    title = models.CharField('наименование', max_length=128)
    description = models.TextField('описание')
    weight = models.IntegerField('вес')
    price = models.DecimalField('цена', max_digits=13, decimal_places=2)
    file_link = models.CharField('файл', max_length=256)
    is_deleted = models.BooleanField(default=False)
    available_objects = AvailableObjectsManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title
