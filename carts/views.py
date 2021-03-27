from django.db.models import Count, Sum
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet

from products.models import Product
from .models import CartProduct, Cart
from .serializers import AddProductSerializer, ProductInCartSerializer, CarWithPriceSerializer


class CartProductViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = CartProduct.objects.select_related('product').all()
    serializer_class = AddProductSerializer

    def get_queryset(self):
        user_id = None if self.request.user.is_anonymous else self.request.user.id
        queryset = super().get_queryset().filter(cart__user_id=user_id)
        if self.action == 'list':
            queryset = Product.objects.filter(cart__user_id=user_id).annotate(quantity=Count('cart_products'))
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductInCartSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        method='get',
        responses={200: CarWithPriceSerializer()}
    )
    @action(detail=False, methods=['get'], url_path='cart-total-price')
    def cart_total_price(self, request, *args, **kwargs):
        user_id = None if self.request.user.is_anonymous else self.request.user.id
        cart_with_price = Cart.objects.prefetch_related('products') \
            .annotate(total_price=Sum('products__price')) \
            .get(user_id=user_id)

        serializer = CarWithPriceSerializer(cart_with_price)
        return Response(serializer.data)
