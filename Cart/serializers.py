from rest_framework import serializers
from base.models import Cart, CartItem,Coupon

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    coupon = serializers.StringRelatedField()  # or use CouponSerializer if needed

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'coupon']
