from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, WishlistItem, Order, OrderItem
from .serializers import CartSerializer, WishlistItemSerializer, OrderSerializer
from products.models import ProductVariant


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


class CartAddItemView(APIView):
    """Add item to cart"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        variant_id = request.data.get('product_variant')
        quantity = request.data.get('quantity', 1)
        
        if not variant_id:
            return Response(
                {'error': 'product_variant is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            variant = ProductVariant.objects.select_related('product').get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {'error': 'Product variant not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock availability
        if variant.stock < quantity:
            return Response(
                {'error': f'Only {variant.stock} items available in stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            status='ACTIVE'
        )
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if variant.stock < new_quantity:
                return Response(
                    {'error': f'Only {variant.stock} items available in stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartUpdateItemView(APIView):
    """Update cart item quantity"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')
        
        if not cart_item_id or quantity is None:
            return Response(
                {'error': 'cart_item_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart_item = CartItem.objects.select_related(
                'cart', 'product_variant'
            ).get(
                id=cart_item_id,
                cart__user=request.user,
                cart__status='ACTIVE'
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        if cart_item.product_variant.stock < quantity:
            return Response(
                {'error': f'Only {cart_item.product_variant.stock} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartSerializer(cart_item.cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartRemoveItemView(APIView):
    """Remove item from cart"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        cart_item_id = request.data.get('cart_item_id')
        
        if not cart_item_id:
            return Response(
                {'error': 'cart_item_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                cart__user=request.user,
                cart__status='ACTIVE'
            )
            cart = cart_item.cart
            cart_item.delete()
            
            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


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



class CheckoutView(APIView):
    """Create order from cart"""
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        shipping_address_id = request.data.get('shipping_address')
        billing_address_id = request.data.get('billing_address')
        
        if not shipping_address_id:
            return Response(
                {'error': 'shipping_address is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get active cart
        try:
            cart = Cart.objects.prefetch_related(
                'items__product_variant__product__vendor'
            ).get(user=request.user, status='ACTIVE')
        except Cart.DoesNotExist:
            return Response(
                {'error': 'No active cart found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate addresses
        from user_accounts.models import Address
        try:
            shipping_address = Address.objects.get(
                id=shipping_address_id,
                user=request.user
            )
            billing_address = shipping_address
            if billing_address_id:
                billing_address = Address.objects.get(
                    id=billing_address_id,
                    user=request.user
                )
        except Address.DoesNotExist:
            return Response(
                {'error': 'Invalid address'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate stock and calculate total
        total = 0
        order_items_data = []
        
        for cart_item in cart.items.all():
            variant = cart_item.product_variant
            
            # Check stock
            if variant.stock < cart_item.quantity:
                return Response(
                    {'error': f'{variant.product.name} - Only {variant.stock} items available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            unit_price = variant.get_price()
            subtotal = unit_price * cart_item.quantity
            total += subtotal
            
            order_items_data.append({
                'variant': variant,
                'quantity': cart_item.quantity,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'vendor': variant.product.vendor
            })
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            total_kes=total,
            status='PENDING_PAYMENT',
            payment_status='PENDING',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product_variant=item_data['variant'],
                vendor=item_data['vendor'],
                unit_price_kes=item_data['unit_price'],
                quantity=item_data['quantity'],
                subtotal_kes=item_data['subtotal']
            )
        
        # Mark cart as checked out
        cart.status = 'CHECKED_OUT'
        cart.save()
        
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishlistRemoveView(APIView):
    """Remove item from wishlist"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            wishlist_item = WishlistItem.objects.get(
                id=pk,
                user=request.user
            )
            wishlist_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WishlistItem.DoesNotExist:
            return Response(
                {'error': 'Wishlist item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
