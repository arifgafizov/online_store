from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from carts.models import CartProduct
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.select_related('cart').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # clearing the shopping cart after saving the order
        if order:
            cart_product = CartProduct.objects.filter(cart_id=order.cart_id)
            cart_product.delete()

    def get_queryset(self):
        user_id = None if self.request.user.is_anonymous else self.request.user.id
        queryset = super().get_queryset().filter(cart__user_id=user_id)
        return queryset
