from django.urls import path
from ..views.api_views import (
    AddCartAPIView,
    GetCartItems,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView
)

urlpatterns = [
    path("add/<int:product_id>/", AddCartAPIView.as_view(), name="add_cart"),
    path("update/<int:cart_item_id>/", UpdateCartItemAPIView.as_view(), name="update_cart"),
    path("delete/<int:cart_item_id>/", DeleteCartItemAPIView.as_view(), name="delete_cart"),
    path("items/", GetCartItems.as_view(), name="cart_items"),
]
