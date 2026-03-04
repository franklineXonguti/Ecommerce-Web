from django.db import models
from django.utils.text import slugify
from common.models import TimeStampedModel


class Vendor(TimeStampedModel):
    owner = models.OneToOneField(
        'user_accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='vendor'
    )
    display_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text="Commission percentage"
    )
    
    class Meta:
        db_table = 'vendors_vendor'
    
    def __str__(self):
        return self.display_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.display_name)
        super().save(*args, **kwargs)


class VendorPayout(TimeStampedModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('REJECTED', 'Rejected'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payouts')
    amount_kes = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference = models.CharField(max_length=100, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'vendors_vendorpayout'
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.vendor.display_name} - {self.amount_kes} KES ({self.status})"
