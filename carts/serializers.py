from rest_framework.serializers import ModelSerializer

from products.serializers import ProductSerializer
from .models import Cart, CartProduct


class CartSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer(many=True)
    cart = CartSerializer(many=True)

    class Meta:
        model = CartProduct
        fields = ['id', 'product','cart']
