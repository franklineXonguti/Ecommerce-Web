from rest_framework import generics, permissions
from .models import Vendor, VendorPayout
from .serializers import VendorSerializer, VendorPayoutSerializer


class VendorDetailView(generics.RetrieveUpdateAPIView):
    """Get and update vendor profile"""
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.vendor


class VendorPayoutListCreateView(generics.ListCreateAPIView):
    """List and create payout requests"""
    serializer_class = VendorPayoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return VendorPayout.objects.filter(vendor=self.request.user.vendor)
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor)
