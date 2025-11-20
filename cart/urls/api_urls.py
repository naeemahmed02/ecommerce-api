from django.urls import path
from cart.views.api_views import ListCartItemsAPIView, AddCartItemAPIView, UpdateCartItemAPIView, DeleteCartItemAPIView

urlpatterns = [
    path("items/<int:product_id>/add/", AddCartItemAPIView.as_view(), name="cart-item-add"),
    path("items/<int:cart_item_id>/", UpdateCartItemAPIView.as_view(), name="cart-item-update"),
    path("items/<int:cart_item_id>/delete/", DeleteCartItemAPIView.as_view(), name="cart-item-delete"),
]
