from rest_framework import serializers
from products.models import Product, ProductVariations


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_single_product",
        lookup_field="slug",
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "url",
            "product_description",
            "price",
            "tax",
            "total_with_tax",
            "image",
            "stock",
            "in_stock",
            "is_active",
            "category",
            "created_at",
            "updated_at",
        ]

class ProductVariaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariations
        fields = "__all__"
