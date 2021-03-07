from django.db import models
from django.utils.translation import ugettext as _


from common.base_model import BaseModel


class Product(BaseModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('product')

    def __str__(self):
        return self.title
