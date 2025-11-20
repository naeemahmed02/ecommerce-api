import logging
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, ProductVariations
from ..models import CartItem
from ..serializers import (
    CartItemSerializer,
    AddCartItemSerializer,
    ProductVariationSimpleSerializer,
)

logger = logging.getLogger(__name__)


class AddCartItemAPIView(APIView):
    """
    POST /api/cart/items/<product_id>/add/
    Body: { "quantity": 1, "variation": [1,2] }
    Authenticated only.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        # validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddCartItemSerializer(data=request.data, context={"product": product})
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            cart_item, created = serializer.create_or_update(request.user, product)

        # prepare response
        variations = list(cart_item.variation.values("id", "variation_category", "variation_value"))
        return Response({
            "success": True,
            "created": created,
            "cart_item": CartItemSerializer(cart_item, context={"request": request}).data,
            "variations": variations
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


class ListCartItemsAPIView(generics.ListAPIView):
    """
    GET /api/cart/items/
    Returns logged-in user's active cart items.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return (
            CartItem.objects
            .select_related("product")
            .prefetch_related("variation")
            .filter(user=self.request.user, is_active=True)
            .order_by("-id")
        )


class UpdateCartItemAPIView(APIView):
    """
    PATCH /api/cart/items/<cart_item_id>/
    Body: { "action": "increase" } or { "action": "decrease" } or { "quantity": 5 }
    Authenticated only.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.select_for_update().get(id=cart_item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")
        explicit_quantity = request.data.get("quantity")

        with transaction.atomic():
            if explicit_quantity is not None:
                try:
                    q = int(explicit_quantity)
                    if q < 1:
                        # delete if zero or negative
                        cart_item.delete()
                        return Response({"success": True, "message": "Item removed"}, status=status.HTTP_200_OK)
                    cart_item.quantity = q
                    cart_item.save()
                except (TypeError, ValueError):
                    return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

            elif action == "increase":
                cart_item.quantity += 1
                cart_item.save()
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    return Response({"success": True, "message": "Item removed"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity
        }, status=status.HTTP_200_OK)


class DeleteCartItemAPIView(APIView):
    """
    DELETE /api/cart/items/<cart_item_id>/
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"success": True, "message": "Item removed from cart"}, status=status.HTTP_200_OK)
