# Release Notes - v0.4.0

**Release Date**: March 4, 2026

## Overview

Version 0.4.0 completes the production-ready infrastructure for SmartCommerce by adding critical missing components: database migrations, comprehensive test suite, HTML email templates, structured logging, and CI/CD pipeline.

## What's New

### Database Migrations
- ✅ Created initial migration files for all Django apps
- ✅ Proper migration dependencies and relationships
- ✅ Migration guide documentation
- ✅ Ready for `python manage.py migrate`

### Comprehensive Test Suite
- ✅ pytest configuration with pytest-django
- ✅ Test fixtures for common objects (users, products, carts, orders)
- ✅ Unit tests for all major models
- ✅ API endpoint tests with authentication
- ✅ Mocked tests for external services (Stripe, M-Pesa, Meilisearch)
- ✅ Test coverage reporting with pytest-cov
- ✅ Testing guide documentation

### HTML Email Templates
- ✅ Base email template with consistent branding
- ✅ Welcome email with verification link
- ✅ Password reset email
- ✅ Order confirmation email
- ✅ Payment receipt email
- ✅ Cart recovery email with coupon code
- ✅ Updated notification tasks to use HTML templates

### Structured Logging
- ✅ Comprehensive logging configuration
- ✅ Separate log files for general logs and errors
- ✅ Rotating file handlers (10MB max, 5 backups)
- ✅ Console and file logging
- ✅ Logging for Django, Celery, and application code
- ✅ Logs directory with .gitkeep

### CI/CD Pipeline
- ✅ GitHub Actions workflow for automated testing
- ✅ PostgreSQL and Redis services in CI
- ✅ Automated linting with flake8
- ✅ Automated test execution
- ✅ Code coverage reporting with Codecov
- ✅ Deployment workflow for tagged releases
- ✅ Docker build in deployment pipeline

## Test Coverage

The test suite covers:
- User registration and authentication
- Email verification system
- Product CRUD operations
- Product variant pricing logic
- Cart operations (add, update, view)
- Order creation and number generation
- Payment processing (Stripe and M-Pesa - mocked)
- Recommendation engine
- Search functionality (Meilisearch - mocked)

## Email Templates

All email templates include:
- Consistent branding with SmartCommerce colors
- Responsive design
- Clear call-to-action buttons
- Plain text fallback
- Professional footer with contact information

## Logging Features

- **Console Logging**: INFO level for development
- **File Logging**: Rotating logs in `backend/logs/django.log`
- **Error Logging**: Separate error log in `backend/logs/errors.log`
- **Celery Logging**: Task execution logs
- **Request Logging**: Django request/response logs

## CI/CD Features

### Continuous Integration
- Runs on push to `main` and `develop` branches
- Runs on pull requests
- PostgreSQL 15 and Redis 7 services
- Python 3.11 environment
- Automated linting and testing
- Coverage reporting

### Deployment Pipeline
- Triggers on version tags (v*.*.*)
- Runs full test suite
- Builds Docker image
- Deployment checklist notification

## Files Added

### Migrations
- `backend/*/migrations/__init__.py` (all apps)
- `backend/*/migrations/0001_initial.py` (all apps)

### Tests
- `backend/conftest.py`
- `backend/pytest.ini`
- `backend/user_accounts/tests.py`
- `backend/products/tests.py`
- `backend/orders/tests.py`
- `backend/payments/tests.py`
- `backend/recommendations/tests.py`
- `backend/search/tests.py`

### Email Templates
- `backend/templates/emails/base.html`
- `backend/templates/emails/welcome.html`
- `backend/templates/emails/password_reset.html`
- `backend/templates/emails/order_confirmation.html`
- `backend/templates/emails/payment_receipt.html`
- `backend/templates/emails/cart_recovery.html`

### CI/CD
- `.github/workflows/django-ci.yml`
- `.github/workflows/deploy.yml`

### Documentation
- `backend/TESTING_GUIDE.md`
- `backend/MIGRATION_GUIDE.md`
- `RELEASE_NOTES_v0.4.0.md`

### Other
- `backend/logs/.gitkeep`

## Files Modified

- `backend/smartcommerce/settings/base.py` - Added logging configuration
- `backend/notifications/tasks.py` - Updated to use HTML email templates
- `backend/requirements/development.txt` - Added pytest-cov
- `backend/.gitignore` - Added coverage.xml and logs exception

## Breaking Changes

None. This release is fully backward compatible.

## Migration Instructions

### For Existing Installations

1. Pull the latest code:
```bash
git pull origin main
```

2. Install new dependencies:
```bash
pip install -r requirements/development.txt
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Create logs directory:
```bash
mkdir -p logs
```

5. Run tests to verify:
```bash
pytest
```

### For New Installations

Follow the updated QUICK_START.md guide.

## Next Steps

The backend is now production-complete with:
- ✅ Complete feature set
- ✅ Database migrations
- ✅ Comprehensive tests
- ✅ Professional email templates
- ✅ Structured logging
- ✅ CI/CD pipeline

Recommended next steps:
1. Deploy to staging environment
2. Run full integration tests
3. Set up monitoring and alerting
4. Configure production email service
5. Set up error tracking (e.g., Sentry)
6. Implement rate limiting for production
7. Set up CDN for static files
8. Configure backup strategy

## Known Issues

None.

## Contributors

- franklineXonguti

## Support

For issues or questions, please open an issue on GitHub or contact support@smartcommerce.com.
