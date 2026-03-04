"""
Payment service utilities
"""
import stripe
import requests
import base64
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Stripe payment service"""
    
    @staticmethod
    def create_checkout_session(order, success_url, cancel_url):
        """Create Stripe checkout session"""
        line_items = []
        
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'kes',
                    'unit_amount': int(item.unit_price_kes * 100),
                    'product_data': {
                        'name': item.product_variant.product.name if item.product_variant else 'Product',
                        'description': f'SKU: {item.product_variant.sku}' if item.product_variant else '',
                    },
                },
                'quantity': item.quantity,
            })
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(order.id),
            customer_email=order.user.email,
            metadata={
                'order_id': order.id,
                'order_number': order.order_number,
            }
        )
        
        return session
    
    @staticmethod
    def verify_webhook_signature(payload, sig_header):
        """Verify Stripe webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            logger.error(f"Webhook signature verification failed: {str(e)}")
            return None


class MPesaService:
    """M-Pesa payment service"""
    
    SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"
    PRODUCTION_BASE_URL = "https://api.safaricom.co.ke"
    
    def __init__(self):
        self.base_url = self.SANDBOX_BASE_URL  # Change to PRODUCTION_BASE_URL for production
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
    
    def get_access_token(self):
        """Get OAuth access token"""
        auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        
        headers = {'Authorization': f'Basic {encoded_auth}'}
        
        try:
            response = requests.get(auth_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get M-Pesa access token: {str(e)}")
            raise
    
    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate STK Push"""
        access_token = self.get_access_token()
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode('utf-8')
        
        stk_push_url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': self.shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc
        }
        
        try:
            response = requests.post(stk_push_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"M-Pesa STK Push failed: {str(e)}")
            raise
    
    def query_transaction_status(self, checkout_request_id):
        """Query STK Push transaction status"""
        access_token = self.get_access_token()
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode('utf-8')
        
        query_url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        try:
            response = requests.post(query_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"M-Pesa query failed: {str(e)}")
            raise
