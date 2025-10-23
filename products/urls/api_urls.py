from django.urls import path
from .. views import api_views

urlpatterns = [
    path('products/', api_views.ProductListAPIView.as_view(), name="products_api"),
    path('products/<str:slug>/', api_views.RetrieveUpdateDestroyAPIViewAPIView.as_view(), name="api_single_product")
]
