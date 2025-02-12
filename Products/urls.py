from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, ProductReviewViewSet,
    WishlistViewSet, AddToWishlistAPIView, RemoveFromWishlistAPIView
)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('reviews', ProductReviewViewSet, basename='reviews')
router.register('wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
    path('wishlist/add/<int:uid>/', AddToWishlistAPIView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:uid>/', RemoveFromWishlistAPIView.as_view(), name='remove_from_wishlist'),
]
