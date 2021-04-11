from datetime import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.models import CartProduct
from online_store.settings import gateway
from orders.models import Order
from orders.orders_constants import ORDER_STATUS_CREATED, ORDER_STATUS_PAID
from orders.serializers import OrderSerializer, PayClientTokenSerializer, PayChekoutSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Order.objects.select_related('cart').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # clearing the shopping cart after saving the order
        cart_product = CartProduct.objects.filter(cart_id=order.cart_id)
        cart_product.delete()

    def get_queryset(self):
        user_id = None if self.request.user.is_anonymous else self.request.user.id
        queryset = super().get_queryset().filter(cart__user_id=user_id)
        return queryset

    @swagger_auto_schema(
        method='post',
        responses={status.HTTP_201_CREATED: PayClientTokenSerializer()},
        request_body=no_body
    )
    @action(detail=True, methods=['post'], url_path='pay-client-token')
    def client_token(self,  request, *args, **kwargs):
        # getting order and validation
        order_id = kwargs['pk']
        order = get_object_or_404(Order, pk=order_id)
        if order.status != ORDER_STATUS_CREATED:
            return Response(data={'reason': f"can't processed order in status {order.status}"}, status=status.HTTP_400_BAD_REQUEST)
        # generate client_token and save it and time of order in DB
        token = gateway.client_token.generate({})
        order.metadata['token'] = token
        order.metadata['time_of_order'] = datetime.now().isoformat()
        order.save()
        return Response(data={'token': token}, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        method='post',
        responses={201: PayChekoutSerializer()},
        request_body=PayChekoutSerializer()
    )
    @action(detail=True, methods=['post'], url_path='pay-chekout')
    def create_purchase(self,  request, *args, **kwargs):
        order_id = kwargs['pk']
        order = get_object_or_404(Order, pk=order_id)
        if order.status != ORDER_STATUS_CREATED:
            return Response(data={'reason': f"can't processed order in status {order.status}"}, status=status.HTTP_400_BAD_REQUEST)

        # TODO Response возвращает объект успешного платежа
        serializer = PayChekoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nonce = serializer.validated_data['nonce']
        #print(serializer.validated_data)
        print(nonce)
        result = gateway.transaction.sale({
            "amount": order.total_price,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        #print(result)

        if result.is_success:
            pass
            # TODO действие по завершению платежа, положить result в метадату, сменить статус заказа на оплачен
            # TODO вернуть объект заказа обернув его в сериализатор
            # order.metadata['result'] = result
            # order.status = ORDER_STATUS_PAID
            # order.save()
            # serializer = self.get_queryset(order)
            return Response('ok', status=status.HTTP_201_CREATED)
        #TODO ELSE вернуть Response(resurn ,400), с причиной отказа например не хватило денег или токен протух, почитать в апи
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # https://articles.braintreepayments.com/control-panel/transactions/declines

        #TODO отдельный вью рендерить шаблон фронтендовой части с формой оплаты, поключить ихнюю библиотеку + axios используя drop-in


class TestPaymentView(TemplateView):
    template_name = 'form.html'
