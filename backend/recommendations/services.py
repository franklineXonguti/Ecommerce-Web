"""
Recommendation engine services
"""
from django.db.models import Count, Q, F
from django.core.cache import cache
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """AI-powered recommendation engine"""
    
    CACHE_TIMEOUT = 3600  # 1 hour
    
    def get_user_recommendations(self, user, limit=10):
        """Get personalized recommendations for user"""
        cache_key = f'user_recommendations_{user.id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        recommendations = []
        
        # Strategy 1: Based on user's purchase history
        purchased_recs = self._recommendations_from_purchases(user, limit=5)
        recommendations.extend(purchased_recs)
        
        # Strategy 2: Based on user's viewed products
        if len(recommendations) < limit:
            viewed_recs = self._recommendations_from_views(user, limit=5)
            recommendations.extend(viewed_recs)
        
        # Strategy 3: Based on user's cart items
        if len(recommendations) < limit:
            cart_recs = self._recommendations_from_cart(user, limit=5)
            recommendations.extend(cart_recs)
        
        # Strategy 4: Popular products in user's favorite categories
        if len(recommendations) < limit:
            category_recs = self._recommendations_from_categories(user, limit=5)
            recommendations.extend(category_recs)
        
        # Strategy 5: Trending products
        if len(recommendations) < limit:
            trending_recs = self._get_trending_products(limit=5)
            recommendations.extend(trending_recs)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for product_id in recommendations:
            if product_id not in seen:
                seen.add(product_id)
                unique_recommendations.append(product_id)
        
        result = unique_recommendations[:limit]
        cache.set(cache_key, result, self.CACHE_TIMEOUT)
        
        return result
    
    def get_product_recommendations(self, product_id, limit=10):
        """Get 'customers also bought' recommendations"""
        cache_key = f'product_recommendations_{product_id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        from orders.models import OrderItem
        from products.models import Product
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return []
        
        # Find orders that contain this product
        orders_with_product = OrderItem.objects.filter(
            product_variant__product_id=product_id,
            order__payment_status='PAID'
        ).values_list('order_id', flat=True)
        
        # Find other products in those orders
        related_products = OrderItem.objects.filter(
            order_id__in=orders_with_product
        ).exclude(
            product_variant__product_id=product_id
        ).values(
            'product_variant__product_id'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        result = [item['product_variant__product_id'] for item in related_products]
        
        # If not enough, add products from same category
        if len(result) < limit:
            category_products = Product.objects.filter(
                category=product.category,
                is_active=True
            ).exclude(
                id=product_id
            ).exclude(
                id__in=result
            ).order_by('-created_at')[:limit - len(result)]
            
            result.extend([p.id for p in category_products])
        
        cache.set(cache_key, result, self.CACHE_TIMEOUT)
        return result
    
    def _recommendations_from_purchases(self, user, limit=5):
        """Recommendations based on purchase history"""
        from orders.models import OrderItem
        from products.models import Product
        
        # Get products user has purchased
        purchased_products = OrderItem.objects.filter(
            order__user=user,
            order__payment_status='PAID'
        ).values_list('product_variant__product_id', flat=True).distinct()
        
        if not purchased_products:
            return []
        
        # Find products frequently bought with user's purchases
        related_orders = OrderItem.objects.filter(
            product_variant__product_id__in=purchased_products,
            order__payment_status='PAID'
        ).values_list('order_id', flat=True)
        
        recommendations = OrderItem.objects.filter(
            order_id__in=related_orders
        ).exclude(
            product_variant__product_id__in=purchased_products
        ).values(
            'product_variant__product_id'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return [item['product_variant__product_id'] for item in recommendations]
    
    def _recommendations_from_views(self, user, limit=5):
        """Recommendations based on viewed products"""
        from .models import UserProductEvent
        from products.models import Product
        
        # Get products user has viewed
        viewed_products = UserProductEvent.objects.filter(
            user=user,
            event_type='VIEW'
        ).values_list('product_id', flat=True).distinct()[:20]
        
        if not viewed_products:
            return []
        
        # Get products from same categories
        viewed_categories = Product.objects.filter(
            id__in=viewed_products
        ).values_list('category_id', flat=True).distinct()
        
        recommendations = Product.objects.filter(
            category_id__in=viewed_categories,
            is_active=True
        ).exclude(
            id__in=viewed_products
        ).order_by('-created_at')[:limit]
        
        return [p.id for p in recommendations]
    
    def _recommendations_from_cart(self, user, limit=5):
        """Recommendations based on cart items"""
        from orders.models import CartItem
        
        # Get products in user's cart
        cart_products = CartItem.objects.filter(
            cart__user=user,
            cart__status='ACTIVE'
        ).values_list('product_variant__product_id', flat=True).distinct()
        
        if not cart_products:
            return []
        
        # Get related products
        recommendations = []
        for product_id in cart_products:
            related = self.get_product_recommendations(product_id, limit=3)
            recommendations.extend(related)
        
        return recommendations[:limit]
    
    def _recommendations_from_categories(self, user, limit=5):
        """Recommendations from user's favorite categories"""
        from .models import UserProductEvent
        from products.models import Product
        
        # Get user's most viewed categories
        viewed_products = UserProductEvent.objects.filter(
            user=user
        ).values_list('product_id', flat=True)[:50]
        
        if not viewed_products:
            return []
        
        category_counts = Product.objects.filter(
            id__in=viewed_products
        ).values('category_id').annotate(
            count=Count('id')
        ).order_by('-count')[:3]
        
        favorite_categories = [item['category_id'] for item in category_counts]
        
        # Get popular products from these categories
        recommendations = Product.objects.filter(
            category_id__in=favorite_categories,
            is_active=True
        ).exclude(
            id__in=viewed_products
        ).order_by('-created_at')[:limit]
        
        return [p.id for p in recommendations]
    
    def _get_trending_products(self, limit=5):
        """Get trending products"""
        from .models import UserProductEvent
        from django.utils import timezone
        from datetime import timedelta
        
        # Products with most events in last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        
        trending = UserProductEvent.objects.filter(
            created_at__gte=week_ago
        ).values('product_id').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return [item['product_id'] for item in trending]
    
    def track_event(self, user, product_id, event_type):
        """Track user product interaction"""
        from .models import UserProductEvent
        
        try:
            UserProductEvent.objects.create(
                user=user if user.is_authenticated else None,
                product_id=product_id,
                event_type=event_type
            )
            
            # Invalidate cache
            if user.is_authenticated:
                cache_key = f'user_recommendations_{user.id}'
                cache.delete(cache_key)
            
            logger.info(f"Tracked {event_type} event for product {product_id}")
        except Exception as e:
            logger.error(f"Error tracking event: {str(e)}")
