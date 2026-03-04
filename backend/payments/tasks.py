"""
Payment-related Celery tasks
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Payment
from .services import MPesaService

logger = logging.getLogger(__name__)


@shared_task
def check_pending_mpesa_payments():
    """Check status of pending M-Pesa payments"""
    # Find payments pending for more than 2 minutes
    cutoff_time = timezone.now() - timedelta(minutes=2)
    
    pending_payments = Payment.objects.filter(
        provider='MPESA',
        status='PENDING',
        created_at__lte=cutoff_time
    )
    
    mpesa_service = MPesaService()
    
    for payment in pending_payments:
        try:
            # Query transaction status
            result = mpesa_service.query_transaction_status(payment.provider_reference)
            
            result_code = result.get('ResultCode')
            
            if result_code == '0':
                # Payment successful
                payment.status = 'SUCCESS'
                payment.raw_response = result
                payment.save()
                
                # Update order
                payment.order.payment_status = 'PAID'
                payment.order.status = 'PROCESSING'
                payment.order.save()
                
                logger.info(f"M-Pesa payment {payment.id} marked as successful")
            elif result_code in ['1032', '1037']:
                # Payment cancelled or timeout
                payment.status = 'FAILED'
                payment.raw_response = result
                payment.save()
                
                payment.order.payment_status = 'FAILED'
                payment.order.save()
                
                logger.info(f"M-Pesa payment {payment.id} marked as failed")
                
        except Exception as e:
            logger.error(f"Error checking M-Pesa payment {payment.id}: {str(e)}")


@shared_task
def process_refund(payment_id):
    """Process payment refund"""
    try:
        payment = Payment.objects.get(id=payment_id)
        
        if payment.status != 'SUCCESS':
            logger.error(f"Cannot refund payment {payment_id} - not successful")
            return
        
        if payment.provider == 'STRIPE':
            # Implement Stripe refund
            import stripe
            from django.conf import settings
            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            refund = stripe.Refund.create(
                payment_intent=payment.provider_reference,
                amount=int(payment.amount_kes * 100)
            )
            
            payment.status = 'REFUNDED'
            payment.raw_response['refund'] = refund
            payment.save()
            
            payment.order.payment_status = 'REFUNDED'
            payment.order.status = 'REFUNDED'
            payment.order.save()
            
            logger.info(f"Stripe refund processed for payment {payment_id}")
            
        elif payment.provider == 'MPESA':
            # M-Pesa refunds require manual processing through Safaricom
            logger.info(f"M-Pesa refund requested for payment {payment_id} - manual processing required")
            
    except Payment.DoesNotExist:
        logger.error(f"Payment {payment_id} not found")
    except Exception as e:
        logger.error(f"Error processing refund for payment {payment_id}: {str(e)}")
