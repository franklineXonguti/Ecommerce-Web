from django.urls import path
from .views import VendorDetailView, VendorPayoutListCreateView

urlpatterns = [
    path('me/', VendorDetailView.as_view(), name='vendor-detail'),
    path('me/payouts/', VendorPayoutListCreateView.as_view(), name='vendor-payouts'),
]
