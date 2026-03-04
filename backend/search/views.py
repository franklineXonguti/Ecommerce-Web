from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import MeilisearchService
import logging

logger = logging.getLogger(__name__)


class ProductSearchView(APIView):
    """Search products using Meilisearch"""
    permission_classes = []
    
    def get(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        vendor = request.query_params.get('vendor', '')
        price_min = request.query_params.get('price_min', '')
        price_max = request.query_params.get('price_max', '')
        sort_by = request.query_params.get('sort', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        # Build filters
        filters = ['is_active = true']
        
        if category:
            filters.append(f'category_id = {category}')
        
        if vendor:
            filters.append(f'vendor_id = {vendor}')
        
        if price_min:
            filters.append(f'price_kes >= {price_min}')
        
        if price_max:
            filters.append(f'price_kes <= {price_max}')
        
        filter_string = ' AND '.join(filters) if filters else None
        
        # Build sort
        sort_string = None
        if sort_by == 'price_asc':
            sort_string = ['price_kes:asc']
        elif sort_by == 'price_desc':
            sort_string = ['price_kes:desc']
        elif sort_by == 'newest':
            sort_string = ['created_at:desc']
        elif sort_by == 'name':
            sort_string = ['name:asc']
        
        # Calculate offset
        offset = (page - 1) * page_size
        
        try:
            # Search
            search_service = MeilisearchService()
            results = search_service.search(
                query=query,
                filters=filter_string,
                sort=sort_string,
                limit=page_size,
                offset=offset
            )
            
            return Response({
                'results': results['hits'],
                'total': results.get('estimatedTotalHits', 0),
                'page': page,
                'page_size': page_size,
                'query': query
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return Response({
                'error': 'Search service unavailable',
                'results': [],
                'total': 0
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
