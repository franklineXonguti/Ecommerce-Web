# SmartCommerce Backend

Django-based e-commerce backend with multi-vendor support, real-time features, and AI recommendations.

## Architecture

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Search**: Meilisearch
- **WebSockets**: Django Channels
- **Background Tasks**: Celery
- **Payments**: Stripe + M-Pesa

## Project Structure

```
backend/
├── smartcommerce/          # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── celery.py
│   ├── asgi.py
│   └── routing.py
├── user_accounts/          # Users, auth, addresses
├── vendors/                # Vendor management
├── products/               # Catalog, inventory
├── orders/                 # Cart, wishlist, orders
├── payments/               # Stripe + M-Pesa
├── recommendations/        # AI recommendations
├── analytics/              # Dashboard metrics
├── search/                 # Meilisearch integration
├── notifications/          # Email, cart recovery
└── common/                 # Shared utilities
```

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

### 2. Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

### 3. Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# In separate terminals:
# Celery worker
celery -A smartcommerce worker -l info

# Celery beat
celery -A smartcommerce beat -l info
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (JWT)
- `POST /api/auth/refresh/` - Refresh token

### User Account
- `GET /api/account/profile/` - Get profile
- `PATCH /api/account/profile/` - Update profile
- `GET /api/account/addresses/` - List addresses
- `POST /api/account/addresses/` - Create address

### Products
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Product details

### Cart & Orders
- `GET /api/cart/` - Get cart
- `GET /api/wishlist/` - Get wishlist
- `GET /api/orders/` - List orders
- `GET /api/orders/{id}/` - Order details

### Payments
- `POST /api/payments/stripe/create-checkout-session/`
- `POST /api/payments/mpesa/stk-push/`

### Search
- `GET /api/search/products/?q=query`

### Recommendations
- `GET /api/recommendations/for-user/`
- `GET /api/recommendations/for-product/{id}/`

### Analytics
- `GET /api/analytics/admin/summary/` - Admin dashboard
- `GET /api/analytics/vendor/summary/` - Vendor dashboard

## WebSocket

Real-time stock updates:
```
ws://localhost:8000/ws/stock/{product_id}/
```

## Development Roadmap

### v0.1.0 - Core (Current)
- [x] Project structure
- [x] User authentication
- [x] Product catalog
- [x] Cart & wishlist
- [ ] Basic orders

### v0.2.0 - Payments
- [ ] Stripe integration
- [ ] M-Pesa integration
- [ ] Real-time stock updates

### v0.3.0 - Intelligence
- [ ] AI recommendations
- [ ] Meilisearch integration
- [ ] Cart recovery emails

### v1.0.0 - Production Ready
- [ ] Analytics dashboards
- [ ] Vendor payouts
- [ ] Security hardening
- [ ] Performance optimization

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=.
```

## Git Workflow

Using Conventional Commits:
- `feat:` New features
- `fix:` Bug fixes
- `chore:` Maintenance
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests

## License

MIT
