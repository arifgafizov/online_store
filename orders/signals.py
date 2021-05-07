from django.db.models import signals
from django.dispatch import receiver

from orders.models import Order
from orders.tasks import send_mail_order_status


@receiver(signal=signals.pre_save, sender=Order)
def pre_save_status(instance, **kwargs):
    original_status = Order.objects.get(pk=instance.pk).status
    instance.context['original_status'] = original_status

@receiver(signal=signals.post_save, sender=Order)
def post_save_status(instance, **kwargs):
    if not instance.status == instance.context['original_status']:
        send_mail_order_status.delay(instance.id, instance.status)
