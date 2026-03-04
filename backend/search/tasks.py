"""
Celery tasks for search indexing
"""
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def sync_product_to_search(product_id):
    """Sync a product to Meilisearch"""
    try:
        from products.models import Product
        from .services import MeilisearchService, product_to_search_document
        
        product = Product.objects.select_related(
            'category', 'vendor'
        ).prefetch_related('images', 'variants').get(id=product_id)
        
        if product.is_active:
            search_service = MeilisearchService()
            document = product_to_search_document(product)
            search_service.index_product(document)
            logger.info(f"Synced product {product_id} to search")
        else:
            # Remove if not active
            remove_product_from_search.delay(product_id)
            
    except Exception as e:
        logger.error(f"Error syncing product {product_id} to search: {str(e)}")


@shared_task
def remove_product_from_search(product_id):
    """Remove a product from Meilisearch"""
    try:
        from .services import MeilisearchService
        
        search_service = MeilisearchService()
        search_service.delete_product(product_id)
        logger.info(f"Removed product {product_id} from search")
        
    except Exception as e:
        logger.error(f"Error removing product {product_id} from search: {str(e)}")


@shared_task
def reindex_all_products():
    """Reindex all active products"""
    try:
        from products.models import Product
        from .services import MeilisearchService, product_to_search_document
        
        products = Product.objects.filter(
            is_active=True
        ).select_related(
            'category', 'vendor'
        ).prefetch_related('images', 'variants')
        
        documents = [product_to_search_document(p) for p in products]
        
        search_service = MeilisearchService()
        search_service.index_products_bulk(documents)
        
        logger.info(f"Reindexed {len(documents)} products")
        return f"Reindexed {len(documents)} products"
        
    except Exception as e:
        logger.error(f"Error reindexing products: {str(e)}")
        raise


@shared_task
def configure_search_index():
    """Configure Meilisearch index settings"""
    try:
        from .services import MeilisearchService
        
        search_service = MeilisearchService()
        search_service.configure_index()
        
        logger.info("Configured search index")
        return "Search index configured"
        
    except Exception as e:
        logger.error(f"Error configuring search index: {str(e)}")
        raise
