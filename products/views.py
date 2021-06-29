from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilter
from .models import Product
from .paginations import ProductPageNumberPagination
from .serializers import ProductSerializer, AddProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    filterset_fields = ['price']
    ordering = ['price']


class AddProductView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class ProductsView(TemplateView):
    template_name = 'products.html'


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'
