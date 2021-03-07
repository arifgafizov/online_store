from django.urls import path

from .views import ProductList, ProductDetail


urlpatterns = [
    path('', ProductList.as_view(), name='products-list'),
    path('<int:pk>/', ProductDetail.as_view(), name='products-detail'),
]