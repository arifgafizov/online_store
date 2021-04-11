from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, TestPaymentView

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
urlpatterns = router.urls
views_urlpatterns = [
  # pylint: disable=invalid-name
  url(r'pay-forms/', TestPaymentView.as_view(), name='pay-forms')]
