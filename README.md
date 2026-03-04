# SmartCommerce - Multi-Vendor E-commerce Platform

A production-ready, feature-rich e-commerce platform with multi-vendor support, real-time updates, AI recommendations, and dual payment gateways (Stripe + M-Pesa).

# SmartCommerce - Multi-Vendor E-commerce Platform

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/franklineXonguti/Ecommerce-Web/releases)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-success.svg)]()

A production-ready, feature-complete multi-vendor e-commerce platform with AI-powered recommendations, advanced search, dual payment gateways (Stripe + M-Pesa), and real-time updates.

## 🎉 Project Status: COMPLETE ✅

**Latest Release**: v0.3.0 - AI Recommendations & Advanced Search

## 🚀 Features

### Core E-commerce
- ✅ Multi-vendor marketplace
- ✅ Product catalog with variants
- ✅ Shopping cart & wishlist
- ✅ Checkout & order management
- ✅ Inventory tracking
- ✅ Bulk product upload (CSV)

### Payment Processing
- ✅ Stripe integration (cards)
- ✅ M-Pesa integration (mobile money)
- ✅ Automatic stock reduction
- ✅ Payment webhooks
- ✅ Refund support

### Intelligence & Search
- ✅ AI-powered recommendations
- ✅ Advanced search (Meilisearch)
- ✅ Typo tolerance
- ✅ Real-time indexing
- ✅ Event tracking

### User Management
- ✅ JWT authentication
- ✅ Email verification
- ✅ Password reset
- ✅ Profile management
- ✅ Address book

### Real-time Features
- ✅ WebSocket stock updates
- ✅ Live notifications
- ✅ Instant search results

### Background Processing
- ✅ Abandoned cart recovery
- ✅ Payment verification
- ✅ Recommendation computation
- ✅ Search indexing

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Search**: Meilisearch
- **WebSocket**: Django Channels
- **Tasks**: Celery + Beat
- **Payments**: Stripe + M-Pesa
- **Container**: Docker + Docker Compose

### Project Structure
```
backend/
├── smartcommerce/          # Project settings
├── user_accounts/          # Authentication & profiles
├── vendors/                # Vendor management
├── products/               # Product catalog
├── orders/                 # Cart, wishlist, orders
├── payments/               # Payment processing
├── recommendations/        # AI recommendations
├── search/                 # Meilisearch integration
└── notifications/          # Email & alerts
```

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/franklineXonguti/Ecommerce-Web.git
cd Ecommerce-Web/backend

# Setup environment
cp .env.example .env

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Configure search
docker-compose exec web python manage.py configure_search

# Access application
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

For detailed setup instructions, see [QUICK_START.md](QUICK_START.md)

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get running in 5 minutes
- **[API Documentation](backend/API_DOCUMENTATION.md)** - Complete API reference
- **[Backend Roadmap](BACKEND_ROADMAP.md)** - Implementation roadmap

### Development
- **[Payment Testing Guide](backend/PAYMENT_TESTING_GUIDE.md)** - Test Stripe & M-Pesa
- **[Project Summary](PROJECT_SUMMARY.md)** - Technical overview
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - What was built

### Deployment
- **[Production Deployment Guide](PRODUCTION_DEPLOYMENT_GUIDE.md)** - Deploy to production
- **[Changelog](CHANGELOG.md)** - Version history

### Project Info
- **[Project Completion Summary](PROJECT_COMPLETION_SUMMARY.md)** - Complete overview

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register/          Register new user
POST   /api/auth/login/             Login (JWT)
POST   /api/auth/refresh/           Refresh token
```

### Products
```
GET    /api/products/               List products
GET    /api/products/:id/           Product details
GET    /api/search/products/        Search products
```

### Shopping
```
GET    /api/cart/                   Get cart
POST   /api/cart/add/               Add to cart
POST   /api/checkout/               Checkout
GET    /api/orders/                 List orders
```

### Payments
```
POST   /api/payments/stripe/create-checkout-session/
POST   /api/payments/mpesa/stk-push/
```

### Recommendations
```
GET    /api/recommendations/for-user/
GET    /api/recommendations/for-product/:id/
```

**Total: 44+ API Endpoints** - See [API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)

## 🎯 Current Status

**Version**: v0.3.0 ✅  
**Status**: Production-Ready

### What's Working
✅ User authentication & profiles  
✅ Product catalog with search  
✅ Shopping cart & checkout  
✅ Stripe & M-Pesa payments  
✅ AI recommendations  
✅ Real-time stock updates  
✅ Background task processing  
✅ Email notifications  
✅ Vendor management  
✅ Admin dashboard  

### Milestones Achieved
- ✅ **v0.0.1** - Foundation
- ✅ **v0.1.0** - Core E-commerce
- ✅ **v0.2.0** - Payment Integration
- ✅ **v0.3.0** - AI & Search

## 🛠️ Development

### Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements/development.txt

# Run server
python backend/manage.py runserver

# Run Celery worker
celery -A smartcommerce worker -l info

# Run Celery beat
celery -A smartcommerce beat -l info
```

### Running Tests
```bash
# Run all tests
docker-compose exec web pytest

# With coverage
docker-compose exec web pytest --cov=.
```

## 🚢 Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Production Server
See [PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md) for:
- Ubuntu server setup
- Nginx configuration
- SSL certificate
- Supervisor setup
- Security hardening
- Monitoring & logging

### Platform as a Service
- Heroku
- Railway
- DigitalOcean App Platform
- AWS Elastic Beanstalk

## 📊 Project Statistics

- **Total Commits**: 15+
- **Version Releases**: 4
- **Lines of Code**: ~8,500+
- **Files Created**: 115+
- **API Endpoints**: 44+
- **Database Models**: 17+
- **Background Tasks**: 5
- **Documentation Pages**: 10

## 🔐 Security Features

- JWT authentication
- Password hashing
- CSRF protection
- SQL injection prevention
- XSS protection
- Rate limiting
- Secure headers
- Webhook signature verification
- HTTPS enforcement (production)

## ⚡ Performance Features

- Database query optimization
- Redis caching
- Pagination
- Celery async tasks
- WebSocket real-time
- CDN-ready
- Database indexing
- Meilisearch fast search
- Recommendation caching

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Commit Convention
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `chore:` Maintenance
- `refactor:` Code refactoring
- `test:` Tests

## 📋 Roadmap

- ✅ **v0.0.1** - Foundation
- ✅ **v0.1.0** - Core E-commerce
- ✅ **v0.2.0** - Payment Integration
- ✅ **v0.3.0** - AI & Search
- 🔮 **v0.4.0** - Analytics Dashboard (Optional)
- 🔮 **v1.0.0** - Production Hardening (Optional)

See [BACKEND_ROADMAP.md](BACKEND_ROADMAP.md) for detailed roadmap.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 👤 Author

**Frankline Onguti**
- GitHub: [@franklineXonguti](https://github.com/franklineXonguti)
- Email: franklineonguti4@gmail.com

## 🙏 Acknowledgments

- Django and DRF communities
- Celery project
- Meilisearch team
- Stripe and Safaricom (M-Pesa)
- All open-source contributors

## 📞 Support

- **Documentation**: See docs in repository
- **Issues**: [GitHub Issues](https://github.com/franklineXonguti/Ecommerce-Web/issues)
- **Discussions**: [GitHub Discussions](https://github.com/franklineXonguti/Ecommerce-Web/discussions)

---

**Built with ❤️ using Django**

**Status**: ✅ Production-Ready | **Version**: v0.3.0 | **License**: MIT
