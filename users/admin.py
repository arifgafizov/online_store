from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import User, PreUser


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         'email',
                                         'middle_name',
                                         'phone_number',
                                         'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',
                       'password1',
                       'password2',
                       'email',
                       'first_name',
                       'last_name',
                       'middle_name',
                       'phone_number',
                       'address'
                       ),
        }),
    )


@admin.register(PreUser)
class PreUserAdmin(admin.ModelAdmin):
    list_display = ['username',
                   'password',
                   'email',
                   'uuid_token',
                   'first_name',
                   'last_name',
                   'middle_name',
                   'phone_number',
                   'address']
    list_filter = ("username", "email")
