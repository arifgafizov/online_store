from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from orders.models import Order

PATH_TO_TEMPLATE_NEW = '/home/arif/PycharmProjects/online_store/online_store/template/email_new.html'
PATH_TO_TEMPLATE_CHANGE = '/home/arif/PycharmProjects/online_store/online_store/template/email_change.html'

@shared_task
def send_mail_create_order(order_id):
    """
       Отправка уведомления о создании заказа по электронной почте.
    """
    order = Order.objects.get(pk=order_id)
    client_name = order.cart.user.first_name
    client_email = order.cart.user.email
    subject = f'Order nr. {order.id}'
    msg_html = render_to_string(PATH_TO_TEMPLATE_NEW, {'client_name': client_name})

    mail_sent = send_mail(subject,
                          None,
                          settings.EMAIL_HOST_USER,
                          [client_email],
                          html_message=msg_html)
    return mail_sent

@shared_task
def send_mail_order_status(order_id, order_status):
    """
       Отправка уведомления о статуса заказа по электронной почте.
    """
    order = Order.objects.get(pk=order_id)
    client_name = order.cart.user.first_name
    client_email = order.cart.user.email
    subject = f'Order nr. {order.id}'
    msg_html = render_to_string(PATH_TO_TEMPLATE_CHANGE, {'client_name': client_name, 'order_status': order_status})

    mail_sent = send_mail(subject,
                          None,
                          settings.EMAIL_HOST_USER,
                          [client_email],
                          html_message=msg_html)
    return mail_sent
