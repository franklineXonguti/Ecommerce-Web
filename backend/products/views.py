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



class VendorProductListCreateView(generics.ListCreateAPIView):
    """List and create products for vendor"""
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Check if user is a vendor
        if not hasattr(self.request.user, 'vendor'):
            return Product.objects.none()
        return Product.objects.filter(vendor=self.request.user.vendor)
    
    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'vendor'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("User is not a vendor")
        serializer.save(vendor=self.request.user.vendor)


class VendorProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete vendor's product"""
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'vendor'):
            return Product.objects.none()
        return Product.objects.filter(vendor=self.request.user.vendor)


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import csv
import io


class BulkProductUploadView(APIView):
    """Bulk upload products via CSV"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not hasattr(request.user, 'vendor'):
            return Response(
                {'error': 'User is not a vendor'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be CSV format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            errors = []
            
            with transaction.atomic():
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate required fields
                        required_fields = ['name', 'description', 'price_kes', 'category_id']
                        missing_fields = [f for f in required_fields if not row.get(f)]
                        
                        if missing_fields:
                            errors.append({
                                'row': row_num,
                                'error': f'Missing fields: {", ".join(missing_fields)}'
                            })
                            continue
                        
                        # Get category
                        from .models import Category
                        try:
                            category = Category.objects.get(id=row['category_id'])
                        except Category.DoesNotExist:
                            errors.append({
                                'row': row_num,
                                'error': f'Category {row["category_id"]} not found'
                            })
                            continue
                        
                        # Create product
                        product = Product.objects.create(
                            vendor=request.user.vendor,
                            name=row['name'],
                            description=row['description'],
                            price_kes=row['price_kes'],
                            category=category,
                            is_active=row.get('is_active', 'true').lower() == 'true'
                        )
                        
                        # Create default variant if SKU provided
                        if row.get('sku'):
                            ProductVariant.objects.create(
                                product=product,
                                sku=row['sku'],
                                stock=int(row.get('stock', 0)),
                                size=row.get('size', ''),
                                color=row.get('color', '')
                            )
                        
                        created_count += 1
                        
                    except Exception as e:
                        errors.append({
                            'row': row_num,
                            'error': str(e)
                        })
            
            return Response({
                'success': True,
                'created_count': created_count,
                'errors': errors
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to process CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
