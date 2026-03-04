from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductVariant
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    """List all active products with filtering"""
    queryset = Product.objects.filter(is_active=True).select_related('category', 'vendor')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'vendor']
    search_fields = ['name', 'description']
    ordering_fields = ['price_kes', 'created_at']
    permission_classes = []


class ProductDetailView(generics.RetrieveAPIView):
    """Get product details"""
    queryset = Product.objects.filter(is_active=True).select_related('category', 'vendor')
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    permission_classes = []
