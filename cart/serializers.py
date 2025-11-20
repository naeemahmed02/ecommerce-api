from rest_framework import serializers
from django.db import transaction

from products.models import Product, ProductVariations
from .models import CartItem


class ProductVariationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariations
        fields = ("id", "variation_category", "variation_value")


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_title = serializers.CharField(source="product.title", read_only=True)  # adjust field name
    variations = ProductVariationSimpleSerializer(source="variation", many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product_id", "product_title", "quantity", "variations", "is_active")


class AddCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, default=1)
    variation = serializers.ListField(
        child=serializers.IntegerField(min_value=1), required=False, default=[]
    )

    def validate(self, data):
        # product is passed in context by view
        product: Product = self.context.get("product")
        variation_ids = data.get("variation", [])

        if variation_ids:
            qs = ProductVariations.objects.filter(id__in=variation_ids)
            if qs.count() != len(set(variation_ids)):
                raise serializers.ValidationError("One or more variation ids are invalid.")
            # ensure all variations belong to the given product
            distinct_products = qs.values_list("product_id", flat=True).distinct()
            if distinct_products.count() != 1 or distinct_products.first() != product.id:
                raise serializers.ValidationError("One or more variations do not belong to the product.")
            data["_validated_variations_qs"] = qs
        else:
            data["_validated_variations_qs"] = ProductVariations.objects.none()

        return data

    def create_or_update(self, user, product):
        """
        This will either update an existing CartItem (same variation set) or create a new one.
        Must be called inside a transaction.
        Returns the cart_item instance and a flag created(bool).
        """
        validated = self.validated_data
        quantity = validated["quantity"]
        variation_qs = validated["_validated_variations_qs"]
        variation_ids = set(variation_qs.values_list("id", flat=True))

        # Prefetch variation relation for efficient comparison
        cart_items = (
            CartItem.objects.filter(user=user, product=product, is_active=True)
            .prefetch_related("variation")
        )

        # build mapping from frozenset(variation_ids) -> cart_item
        mapping = {}
        for item in cart_items:
            item_variation_ids = frozenset(item.variation.values_list("id", flat=True))
            mapping[item_variation_ids] = item

        key = frozenset(variation_ids)
        if key in mapping:
            # Update existing item quantity atomically
            cart_item = mapping[key]
            # Use select_for_update to avoid race conditions
            cart_item = CartItem.objects.select_for_update().get(id=cart_item.id)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item, False
        else:
            cart_item = CartItem.objects.create(product=product, user=user, quantity=quantity)
            if variation_qs.exists():
                cart_item.variation.add(*variation_qs)
            cart_item.save()
            return cart_item, True
