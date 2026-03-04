from rest_framework.views import APIView
from rest_framework.response import Response


class ProductSearchView(APIView):
    """Search products using Meilisearch"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        price_min = request.query_params.get('price_min', '')
        price_max = request.query_params.get('price_max', '')
        
        # TODO: Implement Meilisearch integration
        return Response({
            'results': [],
            'total': 0
        })
