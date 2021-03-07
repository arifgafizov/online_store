from django.db import models
from django.db.models import JSONField


class BaseModel(models.Model):
    """
    Базовая модель, которая содержит общий набор полей для всех моделей проекта.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    additional_info = JSONField("Дополнительные настройки", blank=True, default=dict)

    class Meta:
        """
        Настройки модели.

        Модель является абстрактной.
        """

        abstract = True