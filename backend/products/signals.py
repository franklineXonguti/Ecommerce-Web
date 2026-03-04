from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ProductVariant


@receiver(post_save, sender=ProductVariant)
def broadcast_stock_update(sender, instance, **kwargs):
    """Broadcast stock updates via WebSocket"""
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        f'stock_{instance.product.id}',
        {
            'type': 'stock_update',
            'product_id': instance.product.id,
            'stock': instance.stock
        }
    )
