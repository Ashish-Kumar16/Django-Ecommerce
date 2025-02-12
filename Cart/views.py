from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from base.models import Cart, CartItem, Coupon
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_name = request.data.get('product_name')
        quantity = request.data.get('quantity', 1)
        price = request.data.get('price')

        if not product_name or not price:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            return Response({"detail": "Invalid quantity or price."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0 or price <= 0:
            return Response({"detail": "Quantity and price must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.create(
            cart=cart,
            product_name=product_name,
            quantity=quantity,
            price=price
        )

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        if not quantity:
            return Response({"detail": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"detail": "Invalid quantity."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({"detail": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def remove_coupon(self, request, pk=None):
        """
        Removes the coupon from the cart.
        """
        cart = self.get_object()
        
        if not cart.coupon:
            return Response({"detail": "No coupon applied."}, status=status.HTTP_400_BAD_REQUEST)

        cart.coupon = None
        cart.save()

        return Response({"detail": "Coupon removed successfully."}, status=status.HTTP_200_OK)
