from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel

User = get_user_model()


class UserProductEvent(TimeStampedModel):
    EVENT_TYPES = [
        ('VIEW', 'View'),
        ('ADD_TO_CART', 'Add to Cart'),
        ('PURCHASE', 'Purchase'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    class Meta:
        db_table = 'recommendations_userproductevent'
        indexes = [
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['product', 'event_type']),
        ]
    
    def __str__(self):
        return f"{self.user or 'Anonymous'} - {self.event_type} - {self.product.name}"
