# SmartCommerce Quick Start Guide

Get the backend running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- Git installed
- (Optional) Python 3.11+ for local development

## Option 1: Docker Setup (Recommended)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/franklineXonguti/Ecommerce-Web.git
cd Ecommerce-Web/backend

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings (defaults work for development):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (defaults work with docker-compose)
DB_NAME=smartcommerce
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# For payments (add later)
STRIPE_SECRET_KEY=sk_test_...
MPESA_CONSUMER_KEY=...
```

### 3. Start All Services

```bash
# Start PostgreSQL, Redis, Meilisearch, Django, Celery
docker-compose up -d

# Check logs
docker-compose logs -f web
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
# Enter email, password when prompted
```

### 5. Access the Application

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: See `backend/API_DOCUMENTATION.md`

### 6. Test the API

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 7. Useful Commands

```bash
# Stop services
docker-compose down

# View logs
docker-compose logs -f web
docker-compose logs -f celery-worker

# Restart a service
docker-compose restart web

# Run Django commands
docker-compose exec web python manage.py <command>

# Access Django shell
docker-compose exec web python manage.py shell

# Create migrations
docker-compose exec web python manage.py makemigrations

# Run tests (when added)
docker-compose exec web pytest
```

---

## Option 2: Local Development Setup

### 1. Setup Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt
```

### 2. Setup External Services

You'll need PostgreSQL, Redis, and Meilisearch running locally or use Docker for just these:

```bash
# Start only external services
docker-compose up -d db redis meilisearch
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env - change DB_HOST to localhost if using Docker services
```

### 4. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A smartcommerce worker -l info

# Terminal 3: Celery beat
celery -A smartcommerce beat -l info
```

---

## Next Steps

### 1. Create Sample Data

Access admin panel at http://localhost:8000/admin/ and create:

1. **Categories**: Electronics, Clothing, Books, etc.
2. **Vendor**: Create a vendor account
3. **Products**: Add some products with variants
4. **Addresses**: Add shipping addresses

### 2. Test Core Flows

#### User Registration & Login
```bash
# Register
POST /api/auth/register/

# Login
POST /api/auth/login/

# Get profile
GET /api/account/profile/
Authorization: Bearer <token>
```

#### Browse Products
```bash
# List products
GET /api/products/

# Product details
GET /api/products/1/

# Search
GET /api/search/products/?q=laptop
```

#### Shopping Cart
```bash
# Get cart
GET /api/cart/
Authorization: Bearer <token>

# Add to wishlist
POST /api/wishlist/
Authorization: Bearer <token>
{
  "product": 1
}
```

### 3. Test WebSocket

```javascript
// In browser console or Node.js
const ws = new WebSocket('ws://localhost:8000/ws/stock/1/');

ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => console.log('Stock update:', JSON.parse(event.data));
```

---

## Troubleshooting

### Port Already in Use

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Migration Errors

```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Celery Not Processing Tasks

```bash
# Check Celery worker logs
docker-compose logs celery-worker

# Restart Celery
docker-compose restart celery-worker celery-beat
```

### Import Errors

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Development Tips

### 1. Hot Reload

Django auto-reloads on code changes when using `runserver` or Docker with volume mounts.

### 2. Database GUI

Use tools like:
- pgAdmin: http://localhost:5050 (if added to docker-compose)
- DBeaver
- TablePlus

Connection details from `.env` file.

### 3. API Testing

Use tools like:
- Postman
- Insomnia
- HTTPie
- curl

Import the API documentation to generate requests automatically.

### 4. Debugging

```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use ipdb (better)
import ipdb; ipdb.set_trace()

# View in logs
docker-compose logs -f web
```

### 5. Code Quality

```bash
# Format code
black .

# Lint
flake8

# Type checking (if using mypy)
mypy .
```

---

## Project Structure Overview

```
backend/
├── smartcommerce/          # Project settings & config
│   ├── settings/          # Split settings
│   ├── celery.py          # Celery config
│   ├── asgi.py            # ASGI for WebSockets
│   └── urls.py            # URL routing
│
├── user_accounts/         # Users & auth
├── vendors/               # Vendor management
├── products/              # Catalog & inventory
├── orders/                # Cart, wishlist, orders
├── payments/              # Stripe & M-Pesa
├── recommendations/       # AI recommendations
├── analytics/             # Business intelligence
├── search/                # Meilisearch
├── notifications/         # Emails & alerts
└── common/                # Shared utilities
```

---

## What's Working Now (v0.0.1)

✅ Project structure and configuration
✅ User registration and authentication (JWT)
✅ User profile and address management
✅ Product catalog (list and detail)
✅ Cart and wishlist models
✅ Order models
✅ WebSocket setup for stock updates
✅ Celery task scheduling
✅ Docker containerization

## What's Next (v0.1.0)

🔨 Cart operations (add/update/remove)
🔨 Checkout and order creation
🔨 Vendor product management
🔨 Email verification
🔨 Bulk product upload

See `BACKEND_ROADMAP.md` for complete roadmap.

---

## Getting Help

- **Documentation**: Check `backend/README.md` and `backend/API_DOCUMENTATION.md`
- **Issues**: Report bugs on GitHub Issues
- **Questions**: Use GitHub Discussions

---

## Frontend Integration

Once backend is running, your frontend can connect to:

- **API Base URL**: `http://localhost:8000/api/`
- **WebSocket URL**: `ws://localhost:8000/ws/`
- **Media Files**: `http://localhost:8000/media/`

See `API_DOCUMENTATION.md` for complete endpoint reference with request/response examples.

---

**Happy Coding! 🚀**
