from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


user_model = get_user_model()
class Cart(models.Model):
    products = models.ManyToManyField(to=Product, through="CartProduct", help_text='товар')
    user = models.OneToOneField(user_model, related_name='cart',
                                on_delete=models.CASCADE,
                                help_text='пользователь')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return 'cart of ' + str(self.id)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name='cart_products',
                                on_delete=models.CASCADE,
                                help_text='товар в корзине')
    cart = models.ForeignKey(Cart, related_name='cart_products',
                            on_delete=models.CASCADE,
                            help_text='корзина')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    meta_info = models.JSONField('мета информация', default=dict)
