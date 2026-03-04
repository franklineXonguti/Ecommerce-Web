from django.urls import path
from .views import AdminAnalyticsView, VendorAnalyticsView

urlpatterns = [
    path('admin/summary/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('vendor/summary/', VendorAnalyticsView.as_view(), name='vendor-analytics'),
]
