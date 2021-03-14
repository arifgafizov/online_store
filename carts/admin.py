from django.contrib import admin

from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

    def get_queryset(self, request):
        queryset = Cart.objects.select_related('user')
        return queryset
