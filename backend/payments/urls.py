from django.urls import path
from .views import (
    StripeCheckoutView,
    StripeWebhookView,
    MPesaSTKPushView,
    MPesaCallbackView,
    PaymentStatusView,
    MPesaQueryStatusView
)

urlpatterns = [
    # Stripe
    path('stripe/create-checkout-session/', StripeCheckoutView.as_view(), name='stripe-checkout'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    
    # M-Pesa
    path('mpesa/stk-push/', MPesaSTKPushView.as_view(), name='mpesa-stk-push'),
    path('mpesa/callback/', MPesaCallbackView.as_view(), name='mpesa-callback'),
    path('mpesa/query-status/', MPesaQueryStatusView.as_view(), name='mpesa-query-status'),
    
    # Payment status
    path('status/<int:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),
]
