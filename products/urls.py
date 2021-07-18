from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CRUDProductView


router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('crud-products', CRUDProductView, basename='crud-products')
urlpatterns = router.urls
