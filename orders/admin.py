from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'delivery_at', 'status', 'metadata']
    list_filter = ("delivery_at", "status")

