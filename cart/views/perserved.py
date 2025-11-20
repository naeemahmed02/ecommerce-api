from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from products.models import Product, ProductVariations
from ..models import Cart, CartItem
from rest_framework import generics, permissions
from ..serializers import CartItemSerializer
from rest_framework.response import Response


def _cart_id(request):
    """
    Get or create a unique session key for anonymous users.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    print(f"[DEBUG] Session Cart ID: {cart}")
    return request.session.session_key


class AddCartAPIView(generics.CreateAPIView):
    """
    API to add products to cart with variations.
    Handles:
    - Authenticated users (linked to user)
    - Anonymous users (linked to session cart)
    JSON input:
    {
        "quantity": 1,
        "variation": [1, 2]
    }
    """
    permission_classes = []  # Allow both authenticated & anonymous
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()

    def post(self, request, product_id, *args, **kwargs):
        # --- Fetch product ---
        try:
            product = Product.objects.get(id=product_id)
            print(f"[DEBUG] Product selected: {product}")
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        # --- Parse JSON input ---
        data = request.data
        quantity = int(data.get("quantity", 1))
        variation_ids = data.get("variation", [])
        product_variations = ProductVariations.objects.filter(id__in=variation_ids)
        new_variation_set = set(product_variations.values_list('id', flat=True))
        print(f"[DEBUG] Quantity: {quantity}, Variations to add: {new_variation_set}")

        # --- Determine if user is authenticated ---
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(product=product, user=request.user)
        # else:
        #     # Anonymous user, get or create cart
        #     cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        #     cart_items = CartItem.objects.filter(product=product, cart=cart)

        else:
            return Response({"error": "User not logged in"}, status=401)

        # --- Compare existing items by variation sets ---
        existing_variation_list = [
            set(item.variation.values_list('id', flat=True)) for item in cart_items
        ]
        item_ids = [item.id for item in cart_items]
        print(f"[DEBUG] Existing items variation sets: {existing_variation_list}")

        if new_variation_set in existing_variation_list:
            # Update existing quantity
            index = existing_variation_list.index(new_variation_set)
            item_id = item_ids[index]
            item = CartItem.objects.get(id=item_id)
            item.quantity += quantity
            item.save()
            print(f"[DEBUG] Updated quantity for item {item_id} to {item.quantity}")
            cart_item = item  # For response
        else:
            # Create new CartItem
            if request.user.is_authenticated:
                cart_item = CartItem.objects.create(
                    product=product, quantity=quantity, user=request.user
                )
            # else:
            #     cart_item = CartItem.objects.create(
            #         product=product, quantity=quantity, cart=cart
            #     )
            return Response({"error": "User not logged in"}, status=401)
            if product_variations:
                cart_item.variation.add(*product_variations)
            cart_item.save()
            print(f"[DEBUG] Created new CartItem: {cart_item}")

        # --- Return response ---
        return Response({
            "success": True,
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity,
            "variations": list(product_variations.values('id', 'variation_category', 'variation_value'))
        }, status=200)


    def patch(self, request, product_id, cart_item_id=None, *args, **kwargs):
        # require login
        if not request.user.is_authenticated:
            return Response({
                "error": "User not logged in"
            }, status=401)

        # validate product
        try:
            product = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return Response(
                {
                    "error" : "Product not found"
                }, status=404
            )

        # validate cart item
        try:
            cart_item = CartItem.objects.get(id = cart_item_id, user = request.user, product = product)
        except CartItem.DoesNotExist:
            return Response(
                {
                    "error" : "CartItem not found"
                }, status=404
            )

        # Decrease or remove
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({
            "success": True,
            "message": "Quantity decreased",
            "quantity": cart_item.quantity,
            "cart_item_id": cart_item.id
        }, status=200)

        else:
            cart_item.delete()
            return Response({
                "success": True,
                "message": "Item removed from cart",
            }, status=200)

class DeleteCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=404)

        cart_item.delete()
        return Response({
            "success": True,
            "message": "Item removed from cart"
        }, status=200)

class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, cart_item_id, *args, **kwargs):
        action = request.data.get("action", None)
        # expected: action = "increase" or "decrease"

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=404)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()

        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                return Response({"success": True, "message": "Item removed"}, status=200)
        else:
            return Response({"error": "Invalid action"}, status=400)

        return Response({
            "success": True,
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity
        }, status=200)


class GetCartItems(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return (
            CartItem.objects
            .select_related("product")
            .filter(is_active=True, user=self.request.user)
            .order_by("-id")
        )
