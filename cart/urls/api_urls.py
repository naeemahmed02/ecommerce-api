from django.urls import path
from ..views import api_views

urlpatterns = [
    path('add_cart/<int:product_id>/', api_views.CartAPIView.as_view(), name='add_cart'),
]
