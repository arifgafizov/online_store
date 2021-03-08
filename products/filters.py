from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'gte', 'lt', 'lte', 'exact'],
            'weight': ['gt', 'gte', 'lt', 'lte', 'exact'],
        }
