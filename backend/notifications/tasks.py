from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


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


@shared_task
def send_cart_recovery_email(cart_id):
    """Send cart recovery email"""
    from orders.models import Cart
    
    try:
        cart = Cart.objects.get(id=cart_id)
        if not cart.user:
            return
        
        # TODO: Create coupon and send email with template
        subject = 'Complete your purchase'
        message = f'Hi {cart.user.get_full_name()}, you left items in your cart!'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [cart.user.email],
            fail_silently=False,
        )
    except Cart.DoesNotExist:
        pass
