from rest_framework import serializers # type: ignore
from base.models import Order, OrderItem,ShippingAddress
from Products.serializers import ProductSerializer  # Assuming a ProductSerializer exists
from Accounts.serializers import LoginSerializer  # Assuming a UserSerializer exists

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = LoginSerializer()
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'total_amount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        total_amount = 0
        for item_data in items_data:
            item = OrderItem.objects.create(order=order, **item_data)
            total_amount += item.price * item.quantity

        order.total_amount = total_amount
        order.save()

        return order
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'street', 'street_number', 'zip_code', 'city', 'country', 'phone']