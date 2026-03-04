from django.urls import path
from .views import (
    StripeCheckoutView,
    StripeWebhookView,
    MPesaSTKPushView,
    MPesaCallbackView
)

urlpatterns = [
    path('stripe/create-checkout-session/', StripeCheckoutView.as_view(), name='stripe-checkout'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('mpesa/stk-push/', MPesaSTKPushView.as_view(), name='mpesa-stk-push'),
    path('mpesa/callback/', MPesaCallbackView.as_view(), name='mpesa-callback'),
]
