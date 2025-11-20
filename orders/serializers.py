from rest_framework import serializers
from orders.models import Order, OrderProduct, Payment


class CheckoutSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()

    address_line_one = serializers.CharField()
    address_line_two = serializers.CharField(required=False, allow_blank=True)

    country = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()

    order_note = serializers.CharField(required=False, allow_blank=True)

    order_total = serializers.FloatField()
    tax = serializers.FloatField()


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Payment
        fields = '__all__'

