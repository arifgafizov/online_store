import os

from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from users.models import PreUser

PATH_TO_TEMPLATE_SIGNUP = os.path.join(settings.BASE_DIR, 'template', 'email_signup.html')


@shared_task
def send_mail_signup(pre_user_id):
    """
       Отправка письма с подтверждением регистрации по электронной почте.
    """
    pre_user = PreUser.objects.get(pk=pre_user_id)
    client_uuid = pre_user.uuid_token
    client_email = pre_user.email
    subject = 'Completing sign up'
    msg_html = render_to_string(PATH_TO_TEMPLATE_SIGNUP, {'client_uuid': client_uuid})

    mail_sent = send_mail(subject,
                          None,
                          settings.EMAIL_HOST_USER,
                          [client_email],
                          html_message=msg_html)
    return mail_sent
