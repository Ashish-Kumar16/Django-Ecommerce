from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Include the URLs from different apps
urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),
    
    # Cart-related endpoints
    path('cart/', include('Cart.urls')),  # Include cart URLs from cart app
    
    # User authentication endpoints
    path('accounts/', include('Accounts.urls')),  # Include user authentication URLs from accounts app
    
    # Order-related endpoints
    path('orders/', include('Orders.urls')),  # Include order URLs from orders app
    
    # Product-related endpoints
    path('products/', include('Products.urls')),  # Include product URLs from products app
    
    # You can also add other apps in a similar manner if needed.
]
