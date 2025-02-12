from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from base.models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only get orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Add additional logic for order creation if necessary (e.g., calculating total)
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'Pending':
            return Response({'detail': 'Order cannot be completed.'}, status=400)
        order.status = 'Completed'
        order.save()
        return Response({'detail': 'Order completed successfully.'})

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'Pending':
            return Response({'detail': 'Order cannot be cancelled.'}, status=400)
        order.status = 'Cancelled'
        order.save()
        return Response({'detail': 'Order cancelled successfully.'})
