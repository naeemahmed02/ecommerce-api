from .. models import Order, OrderProduct, Payment
from rest_framework import generics, permissions
from ..serializers import OrderSerializer, OrderProductSerializer, PaymentSerializer

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models import Order, OrderProduct, Payment
from cart.models import CartItem
from ..serializers import CheckoutSerializer, OrderSerializer
import uuid


class CheckoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=400)

        # create order
        order = Order.objects.create(
            user=user,
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            phone=serializer.validated_data["phone"],
            email=serializer.validated_data["email"],
            address_line_one=serializer.validated_data["address_line_one"],
            address_line_two=serializer.validated_data.get("address_line_two", ""),
            country=serializer.validated_data["country"],
            state=serializer.validated_data["state"],
            city=serializer.validated_data["city"],
            order_note=serializer.validated_data.get("order_note", ""),
            tax=serializer.validated_data["tax"],
            order_total=serializer.validated_data["order_total"],
            order_number=str(uuid.uuid4()),
            is_ordered=False
        )

        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=False
            )

            # Add variations properly
            order_product.variation.set(item.variation.all())

            order_product.save()

        # clear cart
        cart_items.delete()

        return Response({
            "message": "Checkout completed. Order created.",
            "order": OrderSerializer(order).data
        }, status=201)



class OrderUpdateRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'id'
    queryset = Order.objects.all()

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(user = self.request.user, is_ordered = True)


class FakePaymentAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method", "Fake Gateway")

        if not order_id:
            return Response({"error": "Order ID is required"}, status=400)

        try:
            order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or already paid"}, status=404)

        # Create a fake payment
        payment = Payment.objects.create(
            user=request.user,
            payment_id=str(uuid.uuid4()),  # fake payment transaction id
            payment_method=payment_method,
            amount_paid=order.order_total,
            status="Paid"
        )

        # Update the order
        order.payment = payment
        order.is_ordered = True
        order.status = "Completed"
        order.save()

        return Response({
            "message": "Payment successful",
            "order_id": order.id,
            "payment_id": payment.payment_id,
            "status": order.status
        }, status=200)