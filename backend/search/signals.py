"""
Signals for syncing products to Meilisearch
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import Product, ProductVariant, ProductImage
from .tasks import sync_product_to_search, remove_product_from_search


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    """Sync product to search index when saved"""
    if created or instance.is_active:
        sync_product_to_search.delay(instance.id)
    elif not instance.is_active:
        # Remove from search if deactivated
        remove_product_from_search.delay(instance.id)


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    """Remove product from search index when deleted"""
    remove_product_from_search.delay(instance.id)


@receiver(post_save, sender=ProductVariant)
def variant_saved(sender, instance, **kwargs):
    """Update product in search when variant changes"""
    sync_product_to_search.delay(instance.product.id)


@receiver(post_save, sender=ProductImage)
def image_saved(sender, instance, **kwargs):
    """Update product in search when image changes"""
    sync_product_to_search.delay(instance.product.id)
