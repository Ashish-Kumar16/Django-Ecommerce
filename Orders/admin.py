# In your app's admin.py (e.g., Accounts or Products)

from django.contrib import admin
from base.models import Order, OrderItem, ShippingAddress

# Register the OrderItem model if it's defined in your app
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_amount')
    inlines = [OrderItemInline]

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'street', 'city', 'zip_code')

# Register the models in the admin interface
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
