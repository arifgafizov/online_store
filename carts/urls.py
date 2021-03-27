from rest_framework.routers import DefaultRouter

from .views import CartProductViewSet

router = DefaultRouter()
router.register('cart-products', CartProductViewSet, basename='cart-product')
urlpatterns = router.urls
