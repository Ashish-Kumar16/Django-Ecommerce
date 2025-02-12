from rest_framework import serializers
from base.models import Product, Category, SizeVariant, SizeVariant, ProductReview, Wishlist, ProductImage, Coupon


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'category_image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Now writable
    product_images = ProductImageSerializer(many=True, read_only=True)
    size_variant = serializers.StringRelatedField(many=True)
    color_variant = serializers.StringRelatedField(many=True)
    rating = serializers.FloatField(source='get_rating', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'category', 'price', 'product_description',  # Fixed typo
            'color_variant', 'size_variant', 'product_images', 'rating'
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='like_count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislike_count', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'stars', 'content', 'date_added', 'likes_count', 'dislikes_count']


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = ProductSerializer()

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'size_variant', 'added_on']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'coupon_code', 'is_expired', 'discount_amount', 'minimum_amount']
