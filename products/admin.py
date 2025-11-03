from django.contrib import admin
from .models import Product, ProductVariations


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
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ("name", "category__name", "price")


@admin.register(ProductVariations)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation_category",
        "variation_value",
        "is_active",
        "created_at",
        "updated_at",
    )