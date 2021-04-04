from django.db import models

from carts.models import Cart
from common.base_model import BaseModel
from orders.orders_constants import ORDER_STATUSES, ORDER_STATUS_CREATED


class Order(BaseModel):
    cart = models.ForeignKey(Cart, related_name='orders', on_delete=models.CASCADE, help_text='корзина заказа')
    delivery_at = models.DateTimeField(verbose_name='дата доставки')
    address = models.CharField('адрес доставки', max_length=200)
    phone = models.CharField('номер телефона', max_length=50)
    status = models.CharField('статус заказа', max_length=100, choices=ORDER_STATUSES, default=ORDER_STATUS_CREATED)
    products = models.JSONField("Продукты заказа", blank=True, default=dict)
    metadata = models.JSONField("Данные заказа", blank=True, default=dict)
    total_price = models.DecimalField("Стоимость заказа", max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.address
