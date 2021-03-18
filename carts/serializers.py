from rest_framework.serializers import ModelSerializer

from products.models import Product
from products.serializers import ProductSerializer
from .models import Cart, CartProduct


class CartSerializer(ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']


class AddProductSerializer(ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'created_at', 'meta_info']
        read_only_fields = ['id', 'created_at', 'meta_info']

    # connecting the current user's shopping cart to add products to their shopping cart
    def validate(self, attrs):
        attrs['cart'] = self.context['request'].user.cart
        return attrs
