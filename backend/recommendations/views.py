from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.models import Product
from products.serializers import ProductListSerializer
from .services import RecommendationEngine
import logging

logger = logging.getLogger(__name__)


class UserRecommendationsView(APIView):
    """Get personalized recommendations for user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        try:
            engine = RecommendationEngine()
            product_ids = engine.get_user_recommendations(request.user, limit=limit)
            
            # Fetch products
            products = Product.objects.filter(
                id__in=product_ids,
                is_active=True
            ).select_related('category', 'vendor').prefetch_related('images')
            
            # Maintain order from recommendations
            products_dict = {p.id: p for p in products}
            ordered_products = [products_dict[pid] for pid in product_ids if pid in products_dict]
            
            serializer = ProductListSerializer(
                ordered_products,
                many=True,
                context={'request': request}
            )
            
            return Response({
                'products': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {str(e)}")
            return Response({
                'products': [],
                'count': 0
            }, status=status.HTTP_200_OK)


class ProductRecommendationsView(APIView):
    """Get 'customers also bought' recommendations"""
    permission_classes = []
    
    def get(self, request, product_id):
        limit = int(request.query_params.get('limit', 10))
        
        try:
            engine = RecommendationEngine()
            product_ids = engine.get_product_recommendations(product_id, limit=limit)
            
            # Fetch products
            products = Product.objects.filter(
                id__in=product_ids,
                is_active=True
            ).select_related('category', 'vendor').prefetch_related('images')
            
            # Maintain order from recommendations
            products_dict = {p.id: p for p in products}
            ordered_products = [products_dict[pid] for pid in product_ids if pid in products_dict]
            
            serializer = ProductListSerializer(
                ordered_products,
                many=True,
                context={'request': request}
            )
            
            return Response({
                'products': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting product recommendations: {str(e)}")
            return Response({
                'products': [],
                'count': 0
            }, status=status.HTTP_200_OK)


class TrackEventView(APIView):
    """Track user product interaction"""
    permission_classes = []
    
    def post(self, request):
        product_id = request.data.get('product_id')
        event_type = request.data.get('event_type', 'VIEW')
        
        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if event_type not in ['VIEW', 'ADD_TO_CART', 'PURCHASE']:
            return Response(
                {'error': 'Invalid event_type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            engine = RecommendationEngine()
            engine.track_event(request.user, product_id, event_type)
            
            return Response(
                {'message': 'Event tracked'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error tracking event: {str(e)}")
            return Response(
                {'error': 'Failed to track event'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
