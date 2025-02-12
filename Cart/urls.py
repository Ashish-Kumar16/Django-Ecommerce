from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

# Create a router instance for DRF viewsets
router = DefaultRouter()
router.register(r'carts', CartViewSet)

urlpatterns = [
    # Cart-related endpoints
    path('cart/', CartViewSet.as_view({'get': 'list'}), name="cart"),  # List all carts
    path('add-to-cart/<int:pk>/', CartViewSet.as_view({'post': 'add_item'}), name="add_to_cart"),  # Add item to cart
    path('update-cart-item/', CartViewSet.as_view({'post': 'update_item'}), name='update_cart_item'),  # Update item in cart
    path('remove-cart/<int:pk>/', CartViewSet.as_view({'post': 'remove_item'}), name="remove_cart"),  # Remove item from cart
    path('remove-coupon/<int:pk>/', CartViewSet.as_view({'post': 'remove_coupon'}), name="remove_coupon"),  # Remove coupon from cart
]

# Add the DRF viewset URL configuration
urlpatterns += router.urls
