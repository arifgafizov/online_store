from rest_framework.generics import ListAPIView, RetrieveAPIView


from .models import Product
from .serializers import ProductSerializer


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #pagination_class = ItemPageNumberPagination
    #filter_backends = [DjangoFilterBackend, OrderingFilter]
    #filterset_class = ItemFilter
    #filterset_fields = ['price']
    #ordering = ['price']


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
