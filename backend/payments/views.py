from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import stripe
import logging

from orders.models import Order
from .models import Payment
from products.models import ProductVariant, InventoryLog

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    """Create Stripe checkout session"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get('order_id')
        
        if not order_id:
            return Response(
                {'error': 'order_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.select_related('user').prefetch_related('items').get(
                id=order_id,
                user=request.user,
                payment_status='PENDING'
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found or already paid'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Create line items for Stripe
            line_items = []
            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'kes',
                        'unit_amount': int(item.unit_price_kes * 100),  # Convert to cents
                        'product_data': {
                            'name': item.product_variant.product.name if item.product_variant else 'Product',
                            'description': f'SKU: {item.product_variant.sku}' if item.product_variant else '',
                        },
                    },
                    'quantity': item.quantity,
                })
            
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f"{settings.FRONTEND_URL}/order-success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/order-cancelled",
                client_reference_id=str(order.id),
                customer_email=request.user.email,
                metadata={
                    'order_id': order.id,
                    'order_number': order.order_number,
                }
            )
            
            # Create payment record
            Payment.objects.create(
                order=order,
                provider='STRIPE',
                provider_reference=checkout_session.id,
                status='PENDING',
                amount_kes=order.total_kes,
                raw_response={'session_id': checkout_session.id}
            )
            
            return Response({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            }, status=status.HTTP_200_OK)
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return Response(
                {'error': f'Payment processing error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return Response(
                {'error': 'Failed to create checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """Handle Stripe webhooks"""
    permission_classes = []
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            logger.error("Invalid payload")
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid signature")
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self._handle_checkout_completed(session)
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            logger.info(f"Payment intent succeeded: {payment_intent['id']}")
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            self._handle_payment_failed(payment_intent)
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def _handle_checkout_completed(self, session):
        """Handle successful checkout"""
        try:
            order_id = session.get('metadata', {}).get('order_id')
            if not order_id:
                order_id = session.get('client_reference_id')
            
            order = Order.objects.select_related('user').prefetch_related(
                'items__product_variant'
            ).get(id=order_id)
            
            # Update payment record
            payment = Payment.objects.get(
                order=order,
                provider_reference=session['id']
            )
            payment.status = 'SUCCESS'
            payment.raw_response = session
            payment.save()
            
            # Update order status
            order.payment_status = 'PAID'
            order.status = 'PROCESSING'
            order.save()
            
            # Reduce stock and create inventory logs
            for item in order.items.all():
                if item.product_variant:
                    variant = item.product_variant
                    variant.stock -= item.quantity
                    variant.save()
                    
                    # Create inventory log
                    InventoryLog.objects.create(
                        product_variant=variant,
                        change=-item.quantity,
                        reason='SALE',
                        note=f'Order {order.order_number}'
                    )
            
            logger.info(f"Order {order.order_number} payment completed")
            
        except Order.DoesNotExist:
            logger.error(f"Order not found for session {session['id']}")
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for session {session['id']}")
        except Exception as e:
            logger.error(f"Error handling checkout completed: {str(e)}")
    
    def _handle_payment_failed(self, payment_intent):
        """Handle failed payment"""
        try:
            # Find payment by provider reference
            payment = Payment.objects.filter(
                provider_reference=payment_intent['id']
            ).first()
            
            if payment:
                payment.status = 'FAILED'
                payment.raw_response = payment_intent
                payment.save()
                
                # Update order
                payment.order.payment_status = 'FAILED'
                payment.order.save()
                
                logger.info(f"Payment failed for order {payment.order.order_number}")
        except Exception as e:
            logger.error(f"Error handling payment failed: {str(e)}")


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



import requests
import base64
from datetime import datetime
from django.utils import timezone


class MPesaSTKPushView(APIView):
    """Initiate M-Pesa STK Push"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get('order_id')
        phone_number = request.data.get('phone_number')
        
        if not order_id or not phone_number:
            return Response(
                {'error': 'order_id and phone_number are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate phone number format (254XXXXXXXXX)
        if not phone_number.startswith('254') or len(phone_number) != 12:
            return Response(
                {'error': 'Phone number must be in format 254XXXXXXXXX'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user,
                payment_status='PENDING'
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found or already paid'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Get M-Pesa access token
            access_token = self._get_mpesa_access_token()
            
            # Prepare STK Push request
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(
                f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
            ).decode('utf-8')
            
            stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': settings.MPESA_SHORTCODE,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(order.total_kes),
                'PartyA': phone_number,
                'PartyB': settings.MPESA_SHORTCODE,
                'PhoneNumber': phone_number,
                'CallBackURL': settings.MPESA_CALLBACK_URL,
                'AccountReference': order.order_number,
                'TransactionDesc': f'Payment for order {order.order_number}'
            }
            
            response = requests.post(stk_push_url, json=payload, headers=headers)
            response_data = response.json()
            
            if response_data.get('ResponseCode') == '0':
                # Create payment record
                Payment.objects.create(
                    order=order,
                    provider='MPESA',
                    provider_reference=response_data.get('CheckoutRequestID'),
                    status='PENDING',
                    amount_kes=order.total_kes,
                    raw_response=response_data
                )
                
                return Response({
                    'message': 'STK push sent successfully',
                    'checkout_request_id': response_data.get('CheckoutRequestID'),
                    'merchant_request_id': response_data.get('MerchantRequestID')
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"M-Pesa STK Push failed: {response_data}")
                return Response(
                    {'error': response_data.get('errorMessage', 'STK push failed')},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"M-Pesa STK Push error: {str(e)}")
            return Response(
                {'error': 'Failed to initiate payment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_mpesa_access_token(self):
        """Get M-Pesa OAuth access token"""
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        
        auth_string = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {encoded_auth}'
        }
        
        response = requests.get(auth_url, headers=headers)
        response_data = response.json()
        
        return response_data.get('access_token')


@method_decorator(csrf_exempt, name='dispatch')
class MPesaCallbackView(APIView):
    """Handle M-Pesa callback"""
    permission_classes = []
    
    @transaction.atomic
    def post(self, request):
        callback_data = request.data
        logger.info(f"M-Pesa callback received: {callback_data}")
        
        try:
            # Extract callback data
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            
            result_code = stk_callback.get('ResultCode')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            
            # Find payment
            try:
                payment = Payment.objects.select_related('order').get(
                    provider_reference=checkout_request_id,
                    provider='MPESA'
                )
            except Payment.DoesNotExist:
                logger.error(f"Payment not found for CheckoutRequestID: {checkout_request_id}")
                return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'}, status=status.HTTP_200_OK)
            
            # Update payment based on result
            if result_code == 0:
                # Payment successful
                payment.status = 'SUCCESS'
                payment.raw_response = callback_data
                
                # Extract M-Pesa receipt number
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                for item in callback_metadata:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        payment.provider_reference = item.get('Value')
                        break
                
                payment.save()
                
                # Update order
                order = payment.order
                order.payment_status = 'PAID'
                order.status = 'PROCESSING'
                order.save()
                
                # Reduce stock
                for item in order.items.all():
                    if item.product_variant:
                        variant = item.product_variant
                        variant.stock -= item.quantity
                        variant.save()
                        
                        # Create inventory log
                        InventoryLog.objects.create(
                            product_variant=variant,
                            change=-item.quantity,
                            reason='SALE',
                            note=f'Order {order.order_number} - M-Pesa'
                        )
                
                logger.info(f"M-Pesa payment successful for order {order.order_number}")
            else:
                # Payment failed
                payment.status = 'FAILED'
                payment.raw_response = callback_data
                payment.save()
                
                payment.order.payment_status = 'FAILED'
                payment.order.save()
                
                logger.info(f"M-Pesa payment failed for order {payment.order.order_number}")
            
            return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"M-Pesa callback error: {str(e)}")
            return Response({'ResultCode': 1, 'ResultDesc': 'Failed'}, status=status.HTTP_200_OK)



class PaymentStatusView(APIView):
    """Check payment status"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.select_related('order').get(
                id=payment_id,
                order__user=request.user
            )
            
            from .serializers import PaymentSerializer
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class MPesaQueryStatusView(APIView):
    """Query M-Pesa transaction status"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        checkout_request_id = request.data.get('checkout_request_id')
        
        if not checkout_request_id:
            return Response(
                {'error': 'checkout_request_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment = Payment.objects.get(
                provider_reference=checkout_request_id,
                provider='MPESA',
                order__user=request.user
            )
            
            # Query M-Pesa
            mpesa_service = MPesaService()
            result = mpesa_service.query_transaction_status(checkout_request_id)
            
            # Update payment if status changed
            result_code = result.get('ResultCode')
            if result_code == '0' and payment.status == 'PENDING':
                payment.status = 'SUCCESS'
                payment.raw_response = result
                payment.save()
                
                payment.order.payment_status = 'PAID'
                payment.order.status = 'PROCESSING'
                payment.order.save()
            
            return Response({
                'status': payment.status,
                'result': result
            }, status=status.HTTP_200_OK)
            
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error querying M-Pesa status: {str(e)}")
            return Response(
                {'error': 'Failed to query payment status'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
