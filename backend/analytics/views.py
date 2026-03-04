from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class AdminAnalyticsView(APIView):
    """Admin dashboard analytics"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # TODO: Implement admin analytics
        return Response({
            'daily_revenue': [],
            'top_products': [],
            'customer_growth': [],
            'orders_by_status': {}
        })


class VendorAnalyticsView(APIView):
    """Vendor dashboard analytics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # TODO: Implement vendor analytics
        return Response({
            'revenue_by_day': [],
            'best_selling_products': [],
            'pending_payouts': 0
        })
