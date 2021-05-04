from celery import shared_task

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from orders.models import Order


@shared_task
def send_mail_order_status(order_id, order_status):
    """
       Отправка уведомления о статуса заказа по электронной почте.
    """
    order = get_object_or_404(Order, pk=order_id)
    client_name = order.cart.user.first_name
    client_email = order.cart.user.email
    subject = f'Order nr. {order.id}'
    message = f'Dear {client_name},\nStatus your order is {order_status}.'

    mail_sent = send_mail(subject,
                          message,
                          'arif_test@rambler.ru',
                          [client_email])
    return mail_sent
