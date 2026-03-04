# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-03-04

### Added
- Database migrations
  - Initial migration files for all Django apps
  - Proper migration dependencies and relationships
  - Migration guide documentation
- Comprehensive test suite
  - pytest configuration with pytest-django
  - Test fixtures for common objects
  - Unit tests for all major models
  - API endpoint tests with authentication
  - Mocked tests for external services (Stripe, M-Pesa, Meilisearch)
  - Test coverage reporting with pytest-cov
  - Testing guide documentation
- HTML email templates
  - Base email template with consistent branding
  - Welcome email with verification link
  - Password reset email
  - Order confirmation email
  - Payment receipt email
  - Cart recovery email with coupon code
- Structured logging
  - Comprehensive logging configuration
  - Separate log files for general logs and errors
  - Rotating file handlers (10MB max, 5 backups)
  - Console and file logging
  - Logging for Django, Celery, and application code
- CI/CD pipeline
  - GitHub Actions workflow for automated testing
  - PostgreSQL and Redis services in CI
  - Automated linting with flake8
  - Automated test execution
  - Code coverage reporting with Codecov
  - Deployment workflow for tagged releases
  - Docker build in deployment pipeline

### Changed
- Updated notification tasks to use HTML email templates
- Enhanced email sending with EmailMultiAlternatives
- Added logging to notification tasks
- Updated .gitignore to exclude logs but keep logs directory
- Added pytest-cov to development requirements

### Documentation
- Added TESTING_GUIDE.md
- Added MIGRATION_GUIDE.md
- Added RELEASE_NOTES_v0.4.0.md
- Updated CHANGELOG.md

## [0.3.0] - 2024-01-01

### Added
- Complete Meilisearch integration
  - MeilisearchService with CRUD operations
  - Automatic product indexing via signals
  - Index configuration (searchable, filterable, sortable attributes)
  - Typo tolerance and ranking rules
  - Real-time sync on product changes
- Advanced product search
  - Search with filters (category, vendor, price range)
  - Multiple sort options (price, date, name)
  - Pagination support
  - Query parameter support
- AI recommendation engine
  - Personalized user recommendations
  - Collaborative filtering algorithm
  - Purchase history analysis
  - View history analysis
  - Cart-based recommendations
  - Category-based recommendations
  - Trending products (7-day window)
  - 'Customers also bought' feature
  - Event tracking (view, cart, purchase)
  - Cache optimization (1-hour TTL)
- Management commands
  - configure_search: Setup Meilisearch index
  - reindex_products: Bulk reindex all products
- Background tasks
  - Precompute user recommendations
  - Precompute product recommendations
  - Batch recommendation computation (daily)
- New API endpoints
  - GET /api/recommendations/for-user/
  - GET /api/recommendations/for-product/:id/
  - POST /api/recommendations/track/
  - Enhanced /api/search/products/

### Changed
- Updated Celery beat schedule with recommendation tasks
- Enhanced search app with signals and tasks

## [0.2.0] - 2024-01-01

### Added
- Complete Stripe payment integration
  - Checkout session creation
  - Webhook handler for payment events
  - Automatic order status updates
  - Stock reduction on payment success
  - Payment verification
- Complete M-Pesa payment integration
  - STK Push implementation
  - OAuth token generation
  - Callback handler
  - Transaction status query
  - Automatic payment verification
- Payment services layer
  - StripeService utility class
  - MPesaService utility class
- Payment endpoints
  - Payment status endpoint
  - M-Pesa query status endpoint
- Background tasks
  - Check pending M-Pesa payments (every 5 minutes)
  - Process refunds
- Payment testing guide
- Payment serializers

### Changed
- Updated Celery beat schedule with payment checks
- Added requests library dependency

## [0.1.0] - 2024-01-01

### Added
- Cart operations (add, update, remove items)
- Checkout endpoint with stock validation
- Vendor product management endpoints
- Bulk product upload via CSV
- Email verification system
- Password reset functionality
- Setup scripts for Windows and Linux/Mac
- API test script

### Changed
- Updated user model with email_verified field
- Enhanced URL routing to avoid conflicts
- Added django-filter dependency

## [0.0.1] - 2024-01-01

### Added
- Initial Django project structure with modular architecture
- Custom user model with JWT authentication
- User registration and login endpoints
- Profile and address management
- Vendor model with approval workflow
- Product catalog with variants and categories (MPTT)
- Inventory logging system
- Shopping cart and wishlist models
- Order management system
- Payment model for Stripe and M-Pesa
- WebSocket consumer for real-time stock updates
- Celery configuration with beat scheduler
- Abandoned cart detection task
- Cart recovery email task
- User event tracking for recommendations
- Analytics endpoint stubs
- Search endpoint stubs
- Docker Compose setup with PostgreSQL, Redis, Meilisearch
- Comprehensive documentation
  - Quick Start Guide
  - Backend Roadmap
  - Project Summary
  - API Documentation
  - Backend README

### Infrastructure
- Split settings (development/production)
- Docker containerization
- Celery worker and beat
- Django Channels for WebSockets
- Admin interfaces for all models

[Unreleased]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/franklineXonguti/Ecommerce-Web/releases/tag/v0.0.1
