from django.contrib import admin
from .models import Cart, CartItem, WishlistItem, Order, OrderItem, Coupon


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [CartItemInline]


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal_kes']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_kes', 'fraud_flag', 'created_at']
    list_filter = ['status', 'payment_status', 'fraud_flag', 'created_at']
    search_fields = ['order_number', 'user__email']
    readonly_fields = ['order_number', 'created_at']
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'discount_amount_kes', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
