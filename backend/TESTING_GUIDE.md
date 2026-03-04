# Testing Guide

This guide covers how to run and write tests for the SmartCommerce backend.

## Test Suite Overview

The project uses pytest with pytest-django for testing. Tests are organized by Django app, with each app having its own `tests.py` file.

## Running Tests

### Prerequisites

1. Install development dependencies:
```bash
pip install -r requirements/development.txt
```

2. Ensure PostgreSQL and Redis are running (via Docker Compose):
```bash
docker-compose up -d postgres redis
```

### Run All Tests

```bash
# From backend directory
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=. --cov-report=html
```

### Run Specific Tests

```bash
# Run tests for a specific app
pytest user_accounts/tests.py

# Run a specific test class
pytest user_accounts/tests.py::TestUserRegistration

# Run a specific test method
pytest user_accounts/tests.py::TestUserRegistration::test_user_registration_success

# Run tests with specific marker
pytest -m unit
pytest -m integration
```

## Test Structure

### Fixtures

Common fixtures are defined in `conftest.py`:
- `api_client`: DRF API client
- `user`: Regular test user
- `vendor_user`: Vendor test user
- `authenticated_client`: Authenticated API client
- `vendor_authenticated_client`: Vendor authenticated API client

### Test Organization

Tests are organized by functionality:

1. **Model Tests**: Test model creation, validation, and methods
2. **API Tests**: Test API endpoints, authentication, and permissions
3. **Service Tests**: Test business logic and external integrations (mocked)
4. **Integration Tests**: Test complete workflows

## Writing Tests

### Example Model Test

```python
import pytest
from myapp.models import MyModel

@pytest.mark.django_db
class TestMyModel:
    def test_model_creation(self):
        obj = MyModel.objects.create(name='Test')
        assert obj.name == 'Test'
```

### Example API Test

```python
import pytest
from rest_framework import status

@pytest.mark.django_db
class TestMyAPI:
    def test_list_endpoint(self, authenticated_client):
        response = authenticated_client.get('/api/myapp/')
        assert response.status_code == status.HTTP_200_OK
```

### Mocking External Services

```python
from unittest.mock import patch, MagicMock

@patch('stripe.checkout.Session.create')
def test_stripe_integration(mock_stripe):
    mock_stripe.return_value = MagicMock(id='test_123')
    # Your test code here
```

## Test Coverage

Current test coverage includes:

- User authentication and registration
- Email verification
- Product CRUD operations
- Cart operations
- Order creation
- Payment processing (Stripe and M-Pesa - mocked)
- Recommendation engine
- Search functionality

### Viewing Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Continuous Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

See `.github/workflows/django-ci.yml` for CI configuration.

## Best Practices

1. **Use fixtures**: Reuse common test data via fixtures
2. **Mock external services**: Don't make real API calls in tests
3. **Test edge cases**: Test both success and failure scenarios
4. **Keep tests isolated**: Each test should be independent
5. **Use descriptive names**: Test names should describe what they test
6. **Mark slow tests**: Use `@pytest.mark.slow` for slow tests
7. **Test permissions**: Verify authentication and authorization

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
# Reset test database
python manage.py flush --noinput
python manage.py migrate
```

### Redis Connection Issues

Ensure Redis is running:
```bash
docker-compose up -d redis
```

### Import Errors

Ensure DJANGO_SETTINGS_MODULE is set:
```bash
export DJANGO_SETTINGS_MODULE=smartcommerce.settings.development
```

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)
- [DRF testing guide](https://www.django-rest-framework.org/api-guide/testing/)
