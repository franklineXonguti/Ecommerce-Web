import pytest
from decimal import Decimal
from orders.models import Cart, CartItem, Order
from products.models import ProductVariant


@pytest.fixture
def cart(db, user):
    """Fixture for creating a cart"""
    return Cart.objects.create(user=user, status='ACTIVE')


@pytest.fixture
def cart_item(db, cart, product_variant):
    """Fixture for creating a cart item"""
    return CartItem.objects.create(
        cart=cart,
        product_variant=product_variant,
        quantity=2
    )


@pytest.mark.django_db
class TestCartModel:
    """Test Cart model"""
    
    def test_cart_creation(self, cart, user):
        """Test cart is created successfully"""
        assert cart.user == user
        assert cart.status == 'ACTIVE'
    
    def test_cart_item_creation(self, cart_item):
        """Test cart item is created successfully"""
        assert cart_item.quantity == 2
        assert cart_item.product_variant.sku == 'TEST-SKU-001'


@pytest.mark.django_db
class TestCartAPI:
    """Test Cart API endpoints"""
    
    def test_add_to_cart(self, authenticated_client, product_variant):
        """Test adding item to cart"""
        data = {
            'product_variant_id': product_variant.id,
            'quantity': 1
        }
        response = authenticated_client.post('/api/cart/add/', data)
        assert response.status_code == 200
        assert Cart.objects.filter(user=authenticated_client.handler._force_user).exists()
    
    def test_add_to_cart_insufficient_stock(self, authenticated_client, product_variant):
        """Test adding more items than available stock"""
        data = {
            'product_variant_id': product_variant.id,
            'quantity': 100  # More than available stock
        }
        response = authenticated_client.post('/api/cart/add/', data)
        assert response.status_code == 400
    
    def test_view_cart(self, authenticated_client, cart, cart_item):
        """Test viewing cart"""
        response = authenticated_client.get('/api/cart/')
        assert response.status_code == 200
        assert len(response.data['items']) > 0


@pytest.mark.django_db
class TestOrderModel:
    """Test Order model"""
    
    def test_order_number_generation(self, user):
        """Test order number is auto-generated"""
        order = Order.objects.create(
            user=user,
            total_kes=Decimal('1000.00'),
            status='PENDING_PAYMENT'
        )
        assert order.order_number.startswith('ORD-')
        assert len(order.order_number) == 16  # ORD- + 12 chars
