from rest_framework.routers import DefaultRouter

from .views import ProductViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
urlpatterns = router.urls
