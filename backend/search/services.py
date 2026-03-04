"""
Meilisearch service for product search
"""
import meilisearch
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MeilisearchService:
    """Meilisearch client wrapper"""
    
    def __init__(self):
        self.client = meilisearch.Client(
            settings.MEILISEARCH_HOST,
            settings.MEILISEARCH_API_KEY
        )
        self.index_name = 'products'
    
    def get_index(self):
        """Get or create products index"""
        try:
            return self.client.get_index(self.index_name)
        except meilisearch.errors.MeilisearchApiError:
            # Create index if it doesn't exist
            task = self.client.create_index(self.index_name, {'primaryKey': 'id'})
            self.client.wait_for_task(task.task_uid)
            return self.client.get_index(self.index_name)
    
    def configure_index(self):
        """Configure index settings"""
        index = self.get_index()
        
        # Searchable attributes
        index.update_searchable_attributes([
            'name',
            'description',
            'category_name',
            'vendor_name',
            'sku'
        ])
        
        # Filterable attributes
        index.update_filterable_attributes([
            'category_id',
            'vendor_id',
            'price_kes',
            'is_active',
            'in_stock'
        ])
        
        # Sortable attributes
        index.update_sortable_attributes([
            'price_kes',
            'created_at',
            'name'
        ])
        
        # Ranking rules
        index.update_ranking_rules([
            'words',
            'typo',
            'proximity',
            'attribute',
            'sort',
            'exactness'
        ])
        
        # Typo tolerance
        index.update_typo_tolerance({
            'enabled': True,
            'minWordSizeForTypos': {
                'oneTypo': 4,
                'twoTypos': 8
            }
        })
        
        logger.info("Meilisearch index configured successfully")
    
    def index_product(self, product_data):
        """Index a single product"""
        try:
            index = self.get_index()
            index.add_documents([product_data])
            logger.info(f"Indexed product {product_data['id']}")
        except Exception as e:
            logger.error(f"Error indexing product: {str(e)}")
    
    def index_products_bulk(self, products_data):
        """Index multiple products"""
        try:
            index = self.get_index()
            task = index.add_documents(products_data)
            logger.info(f"Bulk indexed {len(products_data)} products")
            return task
        except Exception as e:
            logger.error(f"Error bulk indexing products: {str(e)}")
            raise
    
    def update_product(self, product_data):
        """Update a product in the index"""
        try:
            index = self.get_index()
            index.update_documents([product_data])
            logger.info(f"Updated product {product_data['id']}")
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
    
    def delete_product(self, product_id):
        """Delete a product from the index"""
        try:
            index = self.get_index()
            index.delete_document(product_id)
            logger.info(f"Deleted product {product_id}")
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
    
    def search(self, query, filters=None, sort=None, limit=20, offset=0):
        """Search products"""
        try:
            index = self.get_index()
            
            search_params = {
                'limit': limit,
                'offset': offset,
                'attributesToRetrieve': [
                    'id', 'name', 'description', 'price_kes',
                    'category_name', 'vendor_name', 'primary_image',
                    'is_active', 'in_stock'
                ]
            }
            
            if filters:
                search_params['filter'] = filters
            
            if sort:
                search_params['sort'] = sort
            
            results = index.search(query, search_params)
            return results
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return {'hits': [], 'estimatedTotalHits': 0}
    
    def clear_index(self):
        """Clear all documents from index"""
        try:
            index = self.get_index()
            index.delete_all_documents()
            logger.info("Cleared all documents from index")
        except Exception as e:
            logger.error(f"Error clearing index: {str(e)}")


def product_to_search_document(product):
    """Convert product model to search document"""
    from products.models import ProductVariant
    
    # Get primary image
    primary_image = product.images.filter(is_primary=True).first()
    primary_image_url = primary_image.image.url if primary_image else None
    
    # Check if any variant has stock
    has_stock = ProductVariant.objects.filter(
        product=product,
        stock__gt=0
    ).exists()
    
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price_kes': float(product.price_kes),
        'category_id': product.category.id if product.category else None,
        'category_name': product.category.name if product.category else '',
        'vendor_id': product.vendor.id,
        'vendor_name': product.vendor.display_name,
        'primary_image': primary_image_url,
        'is_active': product.is_active,
        'in_stock': has_stock,
        'created_at': product.created_at.timestamp(),
        'sku': ','.join([v.sku for v in product.variants.all()[:5]])  # First 5 SKUs
    }
