from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel
import uuid

User = get_user_model()


class Cart(TimeStampedModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CHECKED_OUT', 'Checked Out'),
        ('ABANDONED', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    class Meta:
        db_table = 'orders_cart'
    
    def __str__(self):
        return f"Cart {self.id} - {self.user or self.session_id}"


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'orders_cartitem'
        unique_together = ['cart', 'product_variant']
    
    def __str__(self):
        return f"{self.quantity}x {self.product_variant.sku}"


class WishlistItem(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders_wishlistitem'
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_PAYMENT')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    
    shipping_address = models.ForeignKey(
        'user_accounts.Address',
        on_delete=models.SET_NULL,
        null=True,
        related_name='shipping_orders'
    )
    billing_address = models.ForeignKey(
        'user_accounts.Address',
        on_delete=models.SET_NULL,
        null=True,
        related_name='billing_orders'
    )
    
    total_kes = models.DecimalField(max_digits=10, decimal_places=2)
    fraud_flag = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'orders_order'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.SET_NULL, null=True)
    unit_price_kes = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal_kes = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'orders_orderitem'
    
    def __str__(self):
        return f"{self.quantity}x {self.product_variant.sku if self.product_variant else 'Deleted Product'}"


class Coupon(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount_kes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'orders_coupon'
    
    def __str__(self):
        return self.code
