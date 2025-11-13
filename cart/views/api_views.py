from django.http import HttpResponse
from products.models import Product, ProductVariations
from ..models import Cart, CartItem
from rest_framework import generics, permissions
from ..serializers import CartItemSerializer
from rest_framework.response import Response
from django.db import transaction


def _cart_id(request):
    """
    Get or create a unique session key for anonymous users.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return request.session.session_key

class AddCartAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()

    def post(self, request, product_id, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated:
            product_variations_list = []
            product = Product.objects.get(id=product_id)
            print(product)
            for key, value in request.POST.items():
                if key in ['csrfmiddlewaretoken']:
                    continue
                try:
                    variation = ProductVariations.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variations_list.append(variation)
                except:
                    pass
            print(f"This is a final list end: {product_variations_list}")
            return HttpResponse("Authenticated user handled" )  # Added return here
        else:
            print('Not authenticated')
            return HttpResponse("Not authenticated")  # Added return here