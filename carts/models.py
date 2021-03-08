from django.db import models
from django.conf import settings

from products.models import Product


class Cart(models.Model):
    products = models.ManyToManyField(to=Product, through="CartProduct")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='carts', on_delete=models.CASCADE)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name='cart_products', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return 'cart of ' + self.user.last_name
