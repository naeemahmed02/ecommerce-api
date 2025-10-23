from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    "name",
    "category",
    "price",
    "tax",
    "total_with_tax",
    "stock",
    "in_stock",
    "created_at",
    "updated_at",
)
    prepopulated_fields = {"slug": ['name']}
    search_fields = ('name', 'category__name', 'price')
