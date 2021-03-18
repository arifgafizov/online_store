from rest_framework.routers import DefaultRouter

from .views import CartViewSet, AddProductViewSet

router = DefaultRouter()
router.register('carts', CartViewSet, basename='cart')
router.register('add-products', AddProductViewSet, basename='add-product')
urlpatterns = router.urls
