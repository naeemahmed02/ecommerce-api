from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock",
        "in_stock",
        "category",
        "tax",
        "created_at",
        "updated_at",
    )
