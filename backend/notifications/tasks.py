from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger('smartcommerce')


@shared_task
def process_abandoned_carts():
    """Find and process abandoned carts"""
    from orders.models import Cart
    from datetime import timedelta
    from django.utils import timezone
    
    # Find carts abandoned for 24+ hours
    cutoff = timezone.now() - timedelta(hours=24)
    abandoned_carts = Cart.objects.filter(
        status='ACTIVE',
        updated_at__lte=cutoff
    )
    
    for cart in abandoned_carts:
        if cart.user and cart.items.exists():
            send_cart_recovery_email.delay(cart.id)
            cart.status = 'ABANDONED'
            cart.save()
            logger.info(f"Marked cart {cart.id} as abandoned for user {cart.user.email}")


@shared_task
def send_cart_recovery_email(cart_id):
    """Send cart recovery email with HTML template"""
    from orders.models import Cart, Coupon
    from datetime import timedelta
    from django.utils import timezone
    
    try:
        cart = Cart.objects.get(id=cart_id)
        if not cart.user:
            return
        
        # Create a recovery coupon (10% off, valid for 48 hours)
        coupon_code = f"RECOVER{cart.id}"
        valid_to = timezone.now() + timedelta(hours=48)
        
        coupon, created = Coupon.objects.get_or_create(
            code=coupon_code,
            defaults={
                'discount_percent': 10,
                'valid_from': timezone.now(),
                'valid_to': valid_to,
                'usage_limit': 1,
                'is_active': True,
            }
        )
        
        # Render HTML email
        context = {
            'user': cart.user,
            'cart': cart,
            'coupon_code': coupon_code,
            'discount': 10,
            'cart_url': f"{settings.FRONTEND_URL}/cart",
        }
        
        html_content = render_to_string('emails/cart_recovery.html', context)
        text_content = f"Hi {cart.user.get_full_name()}, you left items in your cart! Use code {coupon_code} for 10% off."
        
        email = EmailMultiAlternatives(
            subject='Complete Your Purchase - Special Offer Inside!',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cart.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Sent cart recovery email to {cart.user.email} for cart {cart.id}")
        
    except Cart.DoesNotExist:
        logger.error(f"Cart {cart_id} not found for recovery email")
    except Exception as e:
        logger.error(f"Error sending cart recovery email for cart {cart_id}: {str(e)}")


@shared_task
def send_welcome_email(user_id, verification_token):
    """Send welcome email with verification link"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'verification_url': f"{settings.FRONTEND_URL}/verify-email?token={verification_token}",
        }
        
        html_content = render_to_string('emails/welcome.html', context)
        text_content = f"Welcome {user.get_full_name()}! Please verify your email at {context['verification_url']}"
        
        email = EmailMultiAlternatives(
            subject='Welcome to SmartCommerce - Verify Your Email',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Sent welcome email to {user.email}")
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for welcome email")
    except Exception as e:
        logger.error(f"Error sending welcome email to user {user_id}: {str(e)}")


@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email"""
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        context = {
            'order': order,
        }
        
        html_content = render_to_string('emails/order_confirmation.html', context)
        text_content = f"Order {order.order_number} confirmed! Total: KES {order.total_kes}"
        
        email = EmailMultiAlternatives(
            subject=f'Order Confirmation - {order.order_number}',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Sent order confirmation email to {order.user.email} for order {order.order_number}")
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found for confirmation email")
    except Exception as e:
        logger.error(f"Error sending order confirmation email for order {order_id}: {str(e)}")


@shared_task
def send_payment_receipt_email(payment_id):
    """Send payment receipt email"""
    from payments.models import Payment
    
    try:
        payment = Payment.objects.select_related('order', 'order__user').get(id=payment_id)
        
        context = {
            'payment': payment,
            'order': payment.order,
        }
        
        html_content = render_to_string('emails/payment_receipt.html', context)
        text_content = f"Payment received for order {payment.order.order_number}. Amount: KES {payment.amount_kes}"
        
        email = EmailMultiAlternatives(
            subject=f'Payment Receipt - {payment.order.order_number}',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[payment.order.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Sent payment receipt email to {payment.order.user.email} for payment {payment.id}")
        
    except Payment.DoesNotExist:
        logger.error(f"Payment {payment_id} not found for receipt email")
    except Exception as e:
        logger.error(f"Error sending payment receipt email for payment {payment_id}: {str(e)}")
