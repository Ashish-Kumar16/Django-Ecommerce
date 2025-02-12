from django.contrib import admin
from base.models import (
    Category, ColorVariant, SizeVariant, Product, ProductImage,
    Coupon, ProductReview, Wishlist
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_image')


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'slug')  

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ('size_name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'newest_product')
    prepopulated_fields = {'slug': ('product_name',)}
    filter_horizontal = ('color_variant', 'size_variant')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'img_preview')

    def img_preview(self, obj):
        return obj.img_preview()

    img_preview.allow_tags = True
    img_preview.short_description = 'Preview'


# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = ('coupon_code', 'is_expired', 'discount_amount', 'minimum_amount')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'stars', 'date_added', 'like_count', 'dislike_count')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size_variant', 'added_on')
