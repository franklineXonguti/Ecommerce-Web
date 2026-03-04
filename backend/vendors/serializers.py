from rest_framework import serializers
from .models import Vendor, VendorPayout


class VendorSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'display_name', 'slug', 'description', 'is_approved', 
                  'commission_rate', 'owner_email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'is_approved', 'created_at', 'updated_at']


class VendorPayoutSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.display_name', read_only=True)
    
    class Meta:
        model = VendorPayout
        fields = ['id', 'vendor', 'vendor_name', 'amount_kes', 'status', 
                  'reference', 'requested_at', 'processed_at', 'notes']
        read_only_fields = ['id', 'status', 'reference', 'requested_at', 'processed_at']
