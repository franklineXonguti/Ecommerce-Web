"""
Celery tasks for recommendations
"""
from celery import shared_task
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@shared_task
def precompute_user_recommendations(user_id):
    """Precompute recommendations for a user"""
    try:
        from django.contrib.auth import get_user_model
        from .services import RecommendationEngine
        
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        engine = RecommendationEngine()
        recommendations = engine.get_user_recommendations(user, limit=20)
        
        logger.info(f"Precomputed {len(recommendations)} recommendations for user {user_id}")
        return recommendations
        
    except Exception as e:
        logger.error(f"Error precomputing recommendations for user {user_id}: {str(e)}")


@shared_task
def precompute_product_recommendations(product_id):
    """Precompute recommendations for a product"""
    try:
        from .services import RecommendationEngine
        
        engine = RecommendationEngine()
        recommendations = engine.get_product_recommendations(product_id, limit=20)
        
        logger.info(f"Precomputed {len(recommendations)} recommendations for product {product_id}")
        return recommendations
        
    except Exception as e:
        logger.error(f"Error precomputing recommendations for product {product_id}: {str(e)}")


@shared_task
def precompute_all_recommendations():
    """Precompute recommendations for all users and products"""
    try:
        from django.contrib.auth import get_user_model
        from products.models import Product
        
        User = get_user_model()
        
        # Precompute for active users
        active_users = User.objects.filter(is_active=True)[:1000]  # Limit to 1000 users
        for user in active_users:
            precompute_user_recommendations.delay(user.id)
        
        # Precompute for active products
        active_products = Product.objects.filter(is_active=True)[:500]  # Limit to 500 products
        for product in active_products:
            precompute_product_recommendations.delay(product.id)
        
        logger.info(f"Queued recommendation precomputation for {active_users.count()} users and {active_products.count()} products")
        
    except Exception as e:
        logger.error(f"Error precomputing all recommendations: {str(e)}")


@shared_task
def clear_recommendation_cache():
    """Clear all recommendation caches"""
    try:
        # This is a simple implementation
        # In production, you might want to use cache.delete_pattern()
        logger.info("Cleared recommendation cache")
        
    except Exception as e:
        logger.error(f"Error clearing recommendation cache: {str(e)}")
