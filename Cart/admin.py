from django.contrib import admin
from base.models import Cart, CartItem, Coupon
# from base.models import CartItemSerializer, CartSerializer

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # number of empty forms to display by default
    fields = ['product_name', 'quantity', 'price']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'coupon']  # Fields to display in the list view
    inlines = [CartItemInline]  # To show CartItem inline within Cart
    search_fields = ['user__username', 'coupon__code']  # Optional search fields

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'quantity', 'price']  # Fields to display for CartItem
    search_fields = ['product_name']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon)  # Register Coupon model if needed
