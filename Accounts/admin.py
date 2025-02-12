from django.contrib import admin
from django.contrib.auth.models import User
from base.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1  # Add a default empty form for Profile

class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]  # Add Profile as inline to the User admin
    list_display = ['username', 'email', 'is_active', 'is_staff']
    search_fields = ['username', 'email']

# Register User model with the custom UserAdmin
admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, UserAdmin)

# Optionally, register Profile if you need direct control over Profile objects
# admin.site.register(Profile)
