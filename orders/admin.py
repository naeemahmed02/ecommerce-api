from django.contrib import admin
from orders.models import Payment, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'payment', 'email', 'phone', 'status',
        'country', 'state', 'city', 'created_at'
    )

    list_filter = ('status', 'country', 'state', 'city', 'created_at')
    search_fields = ('order_number', 'email', 'phone', 'payment__payment_id')
    list_per_page = 25
    list_select_related = ('payment',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Order Information", {
            "fields": ("order_number", "status")
        }),
        ("Customer", {
            "fields": ("first_name", "last_name", "email", "phone")
        }),
        ("Address", {
            "fields": ("adress_line_one", "adress_line_two", "country", "state", "city")
        }),
        ("Payment", {
            "fields": ("payment",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    search_fields = ('payment_id', 'payment_method')
    list_filter = ('payment_method', 'status', 'created_at')
    list_per_page = 25
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
