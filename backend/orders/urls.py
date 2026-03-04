from django.urls import path
from .views import CartView, WishlistListView, OrderListView, OrderDetailView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
