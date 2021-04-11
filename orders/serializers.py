from django.db.models import Count, Sum
from rest_framework import serializers

from orders.models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id',
                  'status',
                  'phone',
                  'address',
                  'delivery_at',
                  'products',
                  'total_price'
                  ]
        read_only_fields = ['id',
                            'status',
                            'products',
                            'total_price'
                            ]

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        # connecting the current user's shopping cart to make order
        attrs['cart'] = self.context['request'].user.cart

        # connecting products of the current user's shopping cart to make order
        # and changing the product price data type to string
        products = list(Product.objects.filter(cart__user_id=user_id).annotate(quantity=Count('cart_products'))\
            .values('id', 'title', 'price', 'quantity'))
        for product in products:
            product['price'] = str(product['price'])
        attrs['products'] = products

        # connecting total price of the current user's shopping cart to make order
        attrs['total_price'] = Product.objects.filter(cart__user_id=user_id).aggregate(total_price=Sum('price'))\
            ['total_price']
        # checking for the product in the shopping cart
        if len(attrs['products']) == 0:
            raise serializers.ValidationError('корзина для заказа не может быть пустой')
        return attrs


class PayClientTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class PayChekoutSerializer(serializers.Serializer):
    nonce = serializers.CharField()
