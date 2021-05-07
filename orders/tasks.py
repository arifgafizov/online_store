from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string

from orders.models import Order


@shared_task
def send_mail_order_status(order_id, order_status):
    """
       Отправка уведомления о статуса заказа по электронной почте.
    """
    order = Order.objects.get(pk=order_id)
    client_name = order.cart.user.first_name
    client_email = order.cart.user.email
    subject = f'Order nr. {order.id}'
    path_to_template = './online_store/template/email.html'
    msg_html = render_to_string(path_to_template, {'client_name': client_name, 'order_status': order_status})

    mail_sent = send_mail(subject,
                          None,
                          'tab-85@mail.ru',
                          [client_email],
                          html_message=msg_html)
    return mail_sent
