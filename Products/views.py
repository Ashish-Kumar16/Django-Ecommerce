from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from base.models import Product, Category, ProductReview, Wishlist, Coupon
from .serializers import (
    ProductSerializer, CategorySerializer, ProductReviewSerializer,
    WishlistSerializer, CouponSerializer
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('product_images').all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductReviewViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.select_related('product', 'user').all()
    serializer_class = ProductReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class AddToWishlistAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, uid):
        size = request.data.get('size_variant')
        product = get_object_or_404(Product, id=uid)

        if not size:
            return Response({'detail': 'Size variant is required'}, status=400)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product, size_variant_id=size)

        if created:
            return Response({'detail': 'Product added to wishlist'}, status=201)

        return Response({'detail': 'Product already in wishlist'}, status=400)


class RemoveFromWishlistAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, uid):
        size = request.query_params.get('size_variant')
        product = get_object_or_404(Product, id=uid)

        if size:
            Wishlist.objects.filter(user=request.user, product=product, size_variant_id=size).delete()
        else:
            Wishlist.objects.filter(user=request.user, product=product).delete()

        return Response({'detail': 'Product removed from wishlist'}, status=200)
