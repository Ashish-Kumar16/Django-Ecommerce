from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

# Create a router instance for DRF viewsets
router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Order-related endpoints
    path('orders/', OrderViewSet.as_view({'get': 'list'}), name="order_list"),  # List all orders
    path('order/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'}), name="order_detail"),  # View a specific order
    path('create-order/', OrderViewSet.as_view({'post': 'create'}), name="create_order"),  # Create an order
    path('complete-order/<int:pk>/', OrderViewSet.as_view({'post': 'complete_order'}), name="complete_order"),  # Complete an order
    path('cancel-order/<int:pk>/', OrderViewSet.as_view({'post': 'cancel_order'}), name="cancel_order"),  # Cancel an order
]

# Add the DRF viewset URL configuration
urlpatterns += router.urls
