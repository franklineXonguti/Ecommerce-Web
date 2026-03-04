from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, WishlistItem, Order
from .serializers import CartSerializer, WishlistItemSerializer, OrderSerializer


class CartView(generics.RetrieveAPIView):
    """Get current user's active cart"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            status='ACTIVE'
        )
        return cart


class WishlistListView(generics.ListCreateAPIView):
    """List and add items to wishlist"""
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
