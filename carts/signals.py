from django.db.models import signals

from carts.models import Cart, user_model


def create_user(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create(user=instance)

signals.post_save.connect(create_user, sender=user_model)
