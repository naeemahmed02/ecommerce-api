from django.contrib import admin
from .models import Cart, CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'product_name', 'variations_display', 'quantity', 'is_active')
    list_filter = ('is_active', 'user', 'cart')
    search_fields = ('product__name', 'cart__cart_id', 'user__email')

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'

    def variations_display(self, obj):
        # Display comma-separated variations (since it's a ManyToManyField)
        return ", ".join([str(v) for v in obj.variation.all()])
    variations_display.short_description = 'Variations'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'cart_added')
    search_fields = ('cart_id',)
