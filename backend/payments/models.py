from django.db import models
from common.models import TimeStampedModel


class Payment(TimeStampedModel):
    PROVIDER_CHOICES = [
        ('STRIPE', 'Stripe'),
        ('MPESA', 'M-Pesa'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_reference = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    amount_kes = models.DecimalField(max_digits=10, decimal_places=2)
    raw_response = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'payments_payment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.provider} - {self.order.order_number} - {self.status}"
