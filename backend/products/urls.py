from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    VendorProductListCreateView,
    VendorProductDetailView,
    BulkProductUploadView
)

urlpatterns = [
    # Public product endpoints
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Vendor product management
    path('vendor/products/', VendorProductListCreateView.as_view(), name='vendor-product-list'),
    path('vendor/products/<int:pk>/', VendorProductDetailView.as_view(), name='vendor-product-detail'),
    path('vendor/bulk-upload/', BulkProductUploadView.as_view(), name='bulk-upload'),
]
