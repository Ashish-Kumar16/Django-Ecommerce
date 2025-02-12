from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django_countries.fields import CountryField
import os
from django.utils.html import mark_safe

# Custom User model if required
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Specify a unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Specify a unique related name
        blank=True
    )

# BaseModel
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
from django.db import models
from django.utils.text import slugify

# Color Variant model
class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7, blank=True, null=True)  # Optional hex color code
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.color_name)
        super(ColorVariant, self).save(*args, **kwargs)

    def __str__(self):
        return self.color_name


# Size Variant model
class SizeVariant(models.Model):
    size_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.size_name)
        super(SizeVariant, self).save(*args, **kwargs)

    def __str__(self):
        return self.size_name

# Shipping Address
class ShippingAddress(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    country = CountryField()
    phone = models.CharField(max_length=30)
    current_address = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street}, {self.street_number}, {self.city}, {self.country}, {self.zip_code}, {self.phone}'

# Profile model
class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name="shipping_address", null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()

    def save(self, *args, **kwargs):
        if self.pk:  # Only if profile exists
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_image and old_profile.profile_image != self.profile_image:
                    old_image_path = os.path.join(settings.MEDIA_ROOT, old_profile.profile_image.path)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
            except Profile.DoesNotExist:
                pass

        super(Profile, self).save(*args, **kwargs)


# Coupon model
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_amount = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code


# Cart and related models
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Cart {self.id} - User: {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - Quantity: {self.quantity}"


# Order model
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    def calculate_total_amount(self):
        self.total_amount = sum(item.price * item.quantity for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.status}"


# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming Product model exists elsewhere
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product.product_name} for Order {self.order.id}"


# Category and Product models
class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Product(BaseModel):
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField('ColorVariant', blank=True)  # Assuming ColorVariant model exists
    size_variant = models.ManyToManyField('SizeVariant', blank=True)  # Assuming SizeVariant model exists
    newest_product = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


# Product Image model
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product')

    def img_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="500"/>')


# Product Review model
class ProductReview(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    content = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="disliked_reviews", blank=True)

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()


# Wishlist model
class Wishlist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    size_variant = models.ForeignKey('SizeVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name="wishlist_items")  # Assuming SizeVariant model exists
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product", "size_variant"], name="unique_wishlist_item")
        ]

    def __str__(self):
        size = self.size_variant.size_name if self.size_variant else "No Size"
        return f"{self.user.username} - {self.product.product_name} - {size}"
