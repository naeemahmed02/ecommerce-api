from .. models import Order, OrderProduct, Payment
from rest_framework import generics, permissions
from ..serializers import OrderSerializer, OrderProductSerializer, PaymentSerializer


class OrderListAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user, is_ordered = True)

class OrderUpdateRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'id'
    queryset = Order.objects.all()

    def get_queryset(self,*args, **kwargs):
        return Order.objects.filter(user = self.request.user, is_ordered = True)








