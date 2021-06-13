from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product
from .models import Cart, CartProduct


class AddProductSerializer(ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'created_at', 'meta_info']
        read_only_fields = ['id', 'created_at', 'meta_info']

    # connecting the current user's shopping cart to add products to their shopping cart
    def validate(self, attrs):
        attrs['cart'] = self.context['request'].user.cart
        return attrs


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id']


class ProductInCartSerializer(serializers.ModelSerializer):
    quantity = serializers.CharField()
    # saving products using the method 'get_cart_products'
    positions = serializers.SerializerMethodField('get_cart_products')

    # getting products filtered by cart and product to the cart
    def get_cart_products(self, product):
        cart = self.context['request'].user.cart
        cart_products_queryset = CartProduct.objects.filter(cart=cart, product=product)
        serializer = CartProductSerializer(instance=cart_products_queryset, many=True, context=self.context)

        return serializer.data

    class Meta:
        model = Product
        fields = ['id', 'title', 'quantity', 'price', 'positions']


class CarWithPriceSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['total_price']
