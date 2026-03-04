from django.urls import path
from .views import (
    CartView,
    CartAddItemView,
    CartUpdateItemView,
    CartRemoveItemView,
    CheckoutView,
    WishlistListView,
    WishlistRemoveView,
    OrderListView,
    OrderDetailView
)

urlpatterns = [
    # Cart endpoints
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/', CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/remove/', CartRemoveItemView.as_view(), name='cart-remove'),
    
    # Checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    # Wishlist endpoints
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/', WishlistRemoveView.as_view(), name='wishlist-remove'),
    
    # Order endpoints
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
