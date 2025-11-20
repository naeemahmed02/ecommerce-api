from django.urls import path

from orders.views.api_views import OrderUpdateRetrieveDestroyAPIView, CheckoutAPIView, FakePaymentAPIView

urlpatterns = [
    path('order/<int:id>/', OrderUpdateRetrieveDestroyAPIView.as_view(), name='order'),
    path("checkout/", CheckoutAPIView.as_view(), name="checkout"),
    path("<int:id>/", OrderUpdateRetrieveDestroyAPIView.as_view(), name="order-detail"),
    path('payment/', FakePaymentAPIView.as_view(), name='fake-payment'),
]