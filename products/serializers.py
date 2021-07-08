from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'weight', 'price']


class AddNewProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'weight',
            'price',
            'file_link',
            'created_at',
            'updated_at',
            'additional_info']
