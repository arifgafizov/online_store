from datetime import datetime

from django.db import transaction
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
        try:
            order_id = int(order_id)
        except (TypeError, ValueError):
            return Response(data={'reason': "order id is must integer"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        if order.status != ORDER_STATUS_CREATED:
            return Response(data={'reason': f"can't processed order in status {order.status}"},\
                            status=status.HTTP_400_BAD_REQUEST)
        # generate client_token and save it and time of order in DB with isoformat()
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
        # transaction.atomic() гарантирует атомарность операций над БД блока кода
        with transaction.atomic():
            # получение queryset с блокировкой строки до конца завершения транзакции
            order_queryset = Order.objects.select_for_update()
            # getting order and validation
            order = get_object_or_404(order_queryset, pk=order_id)
            if order.status != ORDER_STATUS_CREATED:
                return Response(data={'reason': f"can't processed order in status {order.status}"},\
                                status=status.HTTP_400_BAD_REQUEST)

            # сериализация из запроса nonce
            serializer = PayChekoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            nonce = serializer.validated_data['nonce']

            # создание транзакции с использованием nonce
            result = gateway.transaction.sale({
                "amount": order.total_price,
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            # сбор данных платежа в переменную transaction_data
            transaction_data = {
                'transaction_id': result.transaction.id,
                'credit_card': result.transaction.credit_card,
                'amount': str(result.transaction.amount),
                'currency_iso_code': result.transaction.currency_iso_code,
                'merchant_account_id': result.transaction.merchant_account_id,
                'merchant_address': result.transaction.merchant_address,
                'merchant_identification_number': result.transaction.merchant_identification_number,
                'network_transaction_id': result.transaction.network_transaction_id,
                'updated_at': result.transaction.updated_at.isoformat(),
            }
            # При успешном платеже сохранение transaction_data в метадату в БД и смена статуса заказ на paid
            if result.is_success:
                order.metadata['result'] = transaction_data
                order.status = ORDER_STATUS_PAID
                order.save()
                serializer = self.get_serializer(order)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            # error handler
            errors = []
            for error in result.errors.deep_errors:
                errors.append(error)
            if 'errors' not in order.metadata:
                order.metadata['errors'] = {}
            order.metadata['errors'][result.transaction.id] = errors
            order.save()
            return Response(data={'code_error': 'PAYMENT_TRANSACTION_FAILED', 'errors': errors}, \
                            status=status.HTTP_400_BAD_REQUEST)


class TestPaymentView(TemplateView):
    template_name = 'form.html'

class OrderDetailView(TemplateView):
    template_name = 'order_detail.html'
