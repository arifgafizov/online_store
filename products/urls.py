from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, AddProductView


router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
urlpatterns = [
    path('add-products', AddProductView.as_view({'post': 'create'}), name='add-products')

]
urlpatterns += router.urls
