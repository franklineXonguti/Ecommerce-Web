from django.contrib import admin
from .models import Vendor, VendorPayout


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'owner', 'is_approved', 'commission_rate', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['display_name', 'owner__email']
    readonly_fields = ['slug', 'created_at', 'updated_at']


@admin.register(VendorPayout)
class VendorPayoutAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'amount_kes', 'status', 'requested_at', 'processed_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['vendor__display_name', 'reference']
    readonly_fields = ['requested_at']
