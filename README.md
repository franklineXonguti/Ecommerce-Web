# SmartCommerce - Multi-Vendor E-commerce Platform

A production-ready, feature-rich e-commerce platform with multi-vendor support, real-time updates, AI recommendations, and dual payment gateways (Stripe + M-Pesa).

## 🚀 Features

- **Multi-Vendor Marketplace** - Support for multiple vendors with commission management
- **Real-time Stock Updates** - WebSocket-based live inventory updates
- **AI Recommendations** - Personalized product suggestions and "customers also bought"
- **Advanced Search** - Lightning-fast search powered by Meilisearch
- **Dual Payment Gateways** - Stripe for cards, M-Pesa for mobile money
- **Smart Cart Recovery** - Automated abandoned cart emails with discount codes
- **Comprehensive Analytics** - Dashboards for admins and vendors
- **RESTful API** - Complete API for frontend integration
- **JWT Authentication** - Secure token-based authentication
- **Background Tasks** - Celery for async operations

## 🏗️ Architecture

### Backend Stack
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Search**: Meilisearch
- **WebSockets**: Django Channels
- **Background Tasks**: Celery + Celery Beat
- **Payments**: Stripe + M-Pesa (Daraja API)

### Project Structure
```
backend/
├── smartcommerce/          # Django project settings
├── user_accounts/          # Authentication & profiles
├── vendors/                # Vendor management
├── products/               # Product catalog
├── orders/                 # Cart, wishlist, orders
├── payments/               # Payment processing
├── recommendations/        # AI recommendations
├── analytics/              # Business intelligence
├── search/                 # Search integration
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

# Access application
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

For detailed setup instructions, see [QUICK_START.md](QUICK_START.md)

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[Backend Roadmap](BACKEND_ROADMAP.md)** - Implementation plan and milestones
- **[Project Summary](PROJECT_SUMMARY.md)** - Complete project overview
- **[API Documentation](backend/API_DOCUMENTATION.md)** - Complete API reference
- **[Backend README](backend/README.md)** - Backend-specific documentation

## 🎯 Current Status

**Version**: v0.0.1 ✅  
**Status**: Foundation Complete

### What's Working
✅ Project structure and configuration  
✅ User authentication (JWT)  
✅ Product catalog with variants  
✅ Cart and wishlist  
✅ Order management  
✅ WebSocket setup  
✅ Celery task scheduling  
✅ Docker containerization  

### Next Milestone (v0.1.0)
🔨 Cart operations (add/update/remove)  
🔨 Checkout and order creation  
🔨 Vendor product management  
🔨 Email verification  

See [BACKEND_ROADMAP.md](BACKEND_ROADMAP.md) for complete roadmap.

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
GET    /api/wishlist/               Get wishlist
GET    /api/orders/                 List orders
```

### Payments
```
POST   /api/payments/stripe/create-checkout-session/
POST   /api/payments/mpesa/stk-push/
```

See [API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md) for complete reference.

## 🔄 Real-time Features

### WebSocket Stock Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stock/1/');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Stock update:', data);
  // { product_id: 1, stock: 7 }
};
```

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

### Production Checklist
- [ ] Set `DEBUG=False` in production settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Setup SSL/TLS certificates
- [ ] Configure CORS for frontend domain
- [ ] Setup Sentry for error tracking
- [ ] Configure CDN for static/media files
- [ ] Setup database backups
- [ ] Configure monitoring and alerts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes using conventional commits (`git commit -m 'feat: add amazing feature'`)
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

- **v0.1.0** - Core e-commerce functionality
- **v0.2.0** - Payment integration (Stripe + M-Pesa)
- **v0.3.0** - AI recommendations & advanced search
- **v0.4.0** - Analytics & vendor tools
- **v1.0.0** - Production-ready release

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
- All open-source contributors

---

**Built with ❤️ using Django**
