# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/franklineXonguti/Ecommerce-Web/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/franklineXonguti/Ecommerce-Web/releases/tag/v0.0.1
