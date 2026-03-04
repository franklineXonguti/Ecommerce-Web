from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Address


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_vendor', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_vendor']
    search_fields = ['email', 'first_name', 'last_name', 'business_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Vendor Info', {'fields': ('is_vendor', 'business_name', 'business_registration_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street', 'city', 'county', 'is_default']
    list_filter = ['city', 'county', 'is_default']
    search_fields = ['user__email', 'street', 'city']
