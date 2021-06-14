from django.db.models import signals
from django.dispatch import receiver

from users.models import PreUser
from users.tasks import send_mail_signup


@receiver(signal=signals.post_save, sender=PreUser)
def post_save_signup(instance, **kwargs):
    send_mail_signup.delay(instance.id)
