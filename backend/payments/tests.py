import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from payments.models import Payment
from payments.services import StripeService, MPesaService


@pytest.fixture
def order(db, user):
    """Fixture for creating an order"""
    from orders.models import Order
    return Order.objects.create(
        user=user,
        total_kes=Decimal('1000.00'),
        status='PENDING_PAYMENT'
    )


@pytest.fixture
def payment(db, order):
    """Fixture for creating a payment"""
    return Payment.objects.create(
        order=order,
        provider='STRIPE',
        amount_kes=order.total_kes,
        status='PENDING'
    )


@pytest.mark.django_db
class TestPaymentModel:
    """Test Payment model"""
    
    def test_payment_creation(self, payment, order):
        """Test payment is created successfully"""
        assert payment.order == order
        assert payment.provider == 'STRIPE'
        assert payment.status == 'PENDING'
        assert payment.amount_kes == order.total_kes


@pytest.mark.django_db
class TestStripeService:
    """Test Stripe payment service"""
    
    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_stripe, order):
        """Test creating Stripe checkout session"""
        mock_stripe.return_value = MagicMock(
            id='cs_test_123',
            url='https://checkout.stripe.com/test'
        )
        
        service = StripeService()
        session = service.create_checkout_session(order)
        
        assert session['id'] == 'cs_test_123'
        assert 'url' in session
        mock_stripe.assert_called_once()
    
    @patch('stripe.Refund.create')
    def test_process_refund(self, mock_refund, payment):
        """Test processing Stripe refund"""
        payment.provider_reference = 'pi_test_123'
        payment.status = 'SUCCESS'
        payment.save()
        
        mock_refund.return_value = MagicMock(
            id='re_test_123',
            status='succeeded'
        )
        
        service = StripeService()
        result = service.process_refund(payment)
        
        assert result['success'] is True
        mock_refund.assert_called_once()


@pytest.mark.django_db
class TestMPesaService:
    """Test M-Pesa payment service"""
    
    @patch('requests.post')
    def test_initiate_stk_push(self, mock_post, order):
        """Test initiating M-Pesa STK push"""
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                'ResponseCode': '0',
                'CheckoutRequestID': 'ws_test_123',
                'MerchantRequestID': 'mr_test_123'
            }
        )
        
        service = MPesaService()
        with patch.object(service, 'get_access_token', return_value='test_token'):
            result = service.initiate_stk_push(
                order=order,
                phone_number='254712345678'
            )
        
        assert result['ResponseCode'] == '0'
        assert 'CheckoutRequestID' in result
