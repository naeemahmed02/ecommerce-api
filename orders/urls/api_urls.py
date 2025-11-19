from django.urls import path

from orders.views.api_views import OrderListAPIView, OrderUpdateRetrieveDestroyAPIView

urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list'),
    path('order/<int:id>/', OrderUpdateRetrieveDestroyAPIView.as_view(), name='order'),
]