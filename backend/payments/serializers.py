from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'provider', 'provider_reference',
            'status', 'amount_kes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentStatusSerializer(serializers.Serializer):
    """Serializer for payment status queries"""
    checkout_request_id = serializers.CharField(required=True)
    
    
class RefundRequestSerializer(serializers.Serializer):
    """Serializer for refund requests"""
    payment_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=False, allow_blank=True)
