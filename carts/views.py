from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from .models import Cart, CartProduct
from .serializers import CartSerializer, AddProductSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddProductViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = AddProductSerializer

    # def get_queryset(self):
    #     return Cart.objects.filter(user=self.request.user)
    #     # cart_obj = Cart.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return CartSerializer
    #     else:
    #         return AddProductSerializer

