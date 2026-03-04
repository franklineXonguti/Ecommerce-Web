from rest_framework import serializers
from .models import Cart, CartItem, WishlistItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    price = serializers.DecimalField(source='product_variant.get_price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'product_name', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'status', 'items', 'created_at']


class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price_kes', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_name', 'product_price', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'unit_price_kes', 'subtotal_kes']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'payment_status', 'total_kes', 
                  'shipping_address', 'billing_address', 'items', 'created_at']
        read_only_fields = ['order_number', 'created_at']
