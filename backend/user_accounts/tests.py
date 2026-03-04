import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from user_accounts.tokens import email_verification_token

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_user_registration_success(self, api_client):
        """Test successful user registration"""
        data = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_user_registration_duplicate_email(self, api_client, user):
        """Test registration with duplicate email fails"""
        data = {
            'email': user.email,
            'password': 'securepass123',
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication"""
    
    def test_login_success(self, api_client, user):
        """Test successful login"""
        data = {
            'email': user.email,
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials"""
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestEmailVerification:
    """Test email verification"""
    
    def test_email_verification_token_generation(self, user):
        """Test token generation for email verification"""
        token = email_verification_token.make_token(user)
        assert token is not None
        assert email_verification_token.check_token(user, token)
