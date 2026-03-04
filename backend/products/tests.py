import pytest
from products.models import Category, Product, ProductVariant
from vendors.models import Vendor


@pytest.fixture
def vendor(db, vendor_user):
    """Fixture for creating a vendor"""
    return Vendor.objects.create(
        user=vendor_user,
        name='Test Vendor',
        slug='test-vendor',
        is_active=True
    )


@pytest.fixture
def category(db):
    """Fixture for creating a category"""
    return Category.objects.create(
        name='Electronics',
        slug='electronics'
    )


@pytest.fixture
def product(db, vendor, category):
    """Fixture for creating a product"""
    return Product.objects.create(
        vendor=vendor,
        name='Test Product',
        slug='test-product',
        description='Test description',
        category=category,
        price_kes=1000.00,
        is_active=True
    )


@pytest.fixture
def product_variant(db, product):
    """Fixture for creating a product variant"""
    return ProductVariant.objects.create(
        product=product,
        sku='TEST-SKU-001',
        size='M',
        color='Blue',
        stock=10
    )


@pytest.mark.django_db
class TestProductModel:
    """Test Product model"""
    
    def test_product_creation(self, product):
        """Test product is created successfully"""
        assert product.name == 'Test Product'
        assert product.slug == 'test-product'
        assert product.is_active is True
    
    def test_product_slug_auto_generation(self, vendor, category):
        """Test slug is auto-generated from name"""
        product = Product.objects.create(
            vendor=vendor,
            name='New Product',
            description='Description',
            category=category,
            price_kes=500.00
        )
        assert product.slug == 'new-product'


@pytest.mark.django_db
class TestProductVariantModel:
    """Test ProductVariant model"""
    
    def test_variant_creation(self, product_variant):
        """Test variant is created successfully"""
        assert product_variant.sku == 'TEST-SKU-001'
        assert product_variant.stock == 10
    
    def test_variant_get_price(self, product_variant):
        """Test get_price returns correct price"""
        # Variant has no custom price, should return product price
        assert product_variant.get_price() == product_variant.product.price_kes
        
        # Set custom variant price
        product_variant.price_kes = 1200.00
        product_variant.save()
        assert product_variant.get_price() == 1200.00


@pytest.mark.django_db
class TestProductAPI:
    """Test Product API endpoints"""
    
    def test_list_products(self, api_client, product):
        """Test listing products"""
        response = api_client.get('/api/products/')
        assert response.status_code == 200
        assert len(response.data['results']) > 0
    
    def test_retrieve_product(self, api_client, product):
        """Test retrieving a single product"""
        response = api_client.get(f'/api/products/{product.id}/')
        assert response.status_code == 200
        assert response.data['name'] == product.name
