from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class StripeCheckoutView(APIView):
    """Create Stripe checkout session"""
    def post(self, request):
        # TODO: Implement Stripe checkout
        return Response({'message': 'Stripe integration pending'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class StripeWebhookView(APIView):
    """Handle Stripe webhooks"""
    def post(self, request):
        # TODO: Implement Stripe webhook handler
        return Response({'message': 'Webhook received'}, status=status.HTTP_200_OK)


class MPesaSTKPushView(APIView):
    """Initiate M-Pesa STK Push"""
    def post(self, request):
        # TODO: Implement M-Pesa STK Push
        return Response({'message': 'M-Pesa integration pending'}, status=status.HTTP_501_NOT_IMPLEMENTED)


class MPesaCallbackView(APIView):
    """Handle M-Pesa callback"""
    def post(self, request):
        # TODO: Implement M-Pesa callback handler
        return Response({'message': 'Callback received'}, status=status.HTTP_200_OK)
