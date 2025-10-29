from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = ()