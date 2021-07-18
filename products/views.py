from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import ProductFilter
from .models import Product
from .paginations import ProductPageNumberPagination
from .serializers import ProductSerializer, CRUDProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.available_objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    filterset_fields = ['price']
    ordering = ['price']


class CRUDProductView(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = CRUDProductSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        # product is not deleted and its is_deleted field is assigned True
        instance.is_deleted = True
        instance.save()

class IndexView(TemplateView):
    template_name = 'index.html'


class ProductsView(TemplateView):
    template_name = 'products.html'


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'
