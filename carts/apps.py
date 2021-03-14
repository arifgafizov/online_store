from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'carts'

    def ready(self):
        from .signals import create_user
