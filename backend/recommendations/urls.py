from django.urls import path
from .views import UserRecommendationsView, ProductRecommendationsView, TrackEventView

urlpatterns = [
    path('for-user/', UserRecommendationsView.as_view(), name='user-recommendations'),
    path('for-product/<int:product_id>/', ProductRecommendationsView.as_view(), name='product-recommendations'),
    path('track/', TrackEventView.as_view(), name='track-event'),
]
