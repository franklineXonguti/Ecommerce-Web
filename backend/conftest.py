import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture for DRF API client"""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture for creating a test user"""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        email_verified=True
    )


@pytest.fixture
def vendor_user(db):
    """Fixture for creating a vendor user"""
    return User.objects.create_user(
        email='vendor@example.com',
        password='vendorpass123',
        first_name='Vendor',
        last_name='User',
        is_vendor=True,
        email_verified=True
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture for authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def vendor_authenticated_client(api_client, vendor_user):
    """Fixture for vendor authenticated API client"""
    api_client.force_authenticate(user=vendor_user)
    return api_client
