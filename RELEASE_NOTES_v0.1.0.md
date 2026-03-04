# Release Notes - v0.1.0

**Release Date**: January 2024  
**Status**: Core E-commerce Functionality Complete ✅

## 🎉 Overview

Version 0.1.0 marks the completion of the core e-commerce functionality for SmartCommerce. This release provides a fully functional shopping platform with user management, product catalog, shopping cart, and order processing capabilities.

## ✨ New Features

### 🛒 Shopping Cart Operations
- **Add to Cart**: Add products with stock validation
- **Update Quantity**: Modify cart item quantities with real-time stock checks
- **Remove Items**: Delete items from cart
- **Get Cart**: Retrieve current user's active cart with all items

**API Endpoints**:
```
POST   /api/cart/add/       - Add item to cart
PATCH  /api/cart/update/    - Update cart item quantity
DELETE /api/cart/remove/    - Remove item from cart
GET    /api/cart/           - Get current cart
```

### 💳 Checkout System
- Complete order creation from cart
- Stock availability validation
- Automatic order total calculation
- Order item creation with vendor tracking
- Cart status management (ACTIVE → CHECKED_OUT)
- IP address tracking for fraud detection

**API Endpoint**:
```
POST /api/checkout/
Body: {
  "shipping_address": 1,
  "billing_address": 1  // optional, defaults to shipping
}
```

### 🏪 Vendor Product Management
- List all vendor products
- Create new products
- Update product details
- Delete products
- Bulk upload via CSV

**API Endpoints**:
```
GET    /api/products/vendor/products/        - List vendor products
POST   /api/products/vendor/products/        - Create product
GET    /api/products/vendor/products/:id/    - Get product
PATCH  /api/products/vendor/products/:id/    - Update product
DELETE /api/products/vendor/products/:id/    - Delete product
POST   /api/products/vendor/bulk-upload/     - Bulk upload CSV
```

**CSV Format**:
```csv
name,description,price_kes,category_id,sku,stock,size,color,is_active
Product Name,Description,1000,1,SKU-001,10,Medium,Blue,true
```

### ✉️ Email Verification System
- Send verification email with secure token
- Email verification endpoint
- 24-hour token expiration
- Automatic email on registration (optional)

**API Endpoints**:
```
POST /api/auth/send-verification/    - Send verification email
POST /api/auth/verify-email/         - Verify email with token
Body: { "uid": "...", "token": "..." }
```

### 🔐 Password Reset
- Request password reset via email
- Secure token-based reset
- 24-hour token expiration
- Email doesn't reveal if account exists (security)

**API Endpoints**:
```
POST /api/auth/password-reset/          - Request reset
POST /api/auth/password-reset-confirm/  - Confirm reset
```

### ❤️ Wishlist Management
- Add products to wishlist
- Remove from wishlist
- List all wishlist items

**API Endpoints**:
```
GET    /api/wishlist/        - List wishlist
POST   /api/wishlist/        - Add to wishlist
DELETE /api/wishlist/:id/    - Remove from wishlist
```

## 🛠️ Developer Tools

### Setup Scripts
- **setup.sh** (Linux/Mac): Automated setup script
- **setup.ps1** (Windows): PowerShell setup script
- Automatic .env creation
- Docker service startup
- Database migration
- Superuser creation

**Usage**:
```bash
# Linux/Mac
chmod +x backend/setup.sh
./backend/setup.sh

# Windows
.\backend\setup.ps1
```

### API Test Script
- Quick API testing tool
- Tests all major endpoints
- Validates authentication flow
- Pretty-printed responses

**Usage**:
```bash
python backend/test_api.py
```

## 🔧 Technical Improvements

### Database Schema Updates
- Added `email_verified` field to CustomUser model
- Enhanced cart item validation
- Order item vendor tracking

### Dependencies
- Added `django-filter` for advanced filtering
- Added `six` for Python 2/3 compatibility

### URL Routing
- Reorganized URL patterns to avoid conflicts
- Cleaner API structure
- Namespace support for account endpoints

## 📊 API Summary

### Complete Endpoint List

**Authentication**:
- POST `/api/auth/register/` - Register
- POST `/api/auth/login/` - Login
- POST `/api/auth/refresh/` - Refresh token
- POST `/api/auth/send-verification/` - Send verification
- POST `/api/auth/verify-email/` - Verify email
- POST `/api/auth/password-reset/` - Request reset
- POST `/api/auth/password-reset-confirm/` - Confirm reset

**User Profile**:
- GET `/api/account/profile/` - Get profile
- PATCH `/api/account/profile/` - Update profile
- GET `/api/account/addresses/` - List addresses
- POST `/api/account/addresses/` - Create address
- GET `/api/account/addresses/:id/` - Get address
- PATCH `/api/account/addresses/:id/` - Update address
- DELETE `/api/account/addresses/:id/` - Delete address

**Products**:
- GET `/api/products/` - List products
- GET `/api/products/:id/` - Product details

**Vendor Products**:
- GET `/api/products/vendor/products/` - List vendor products
- POST `/api/products/vendor/products/` - Create product
- GET `/api/products/vendor/products/:id/` - Get product
- PATCH `/api/products/vendor/products/:id/` - Update product
- DELETE `/api/products/vendor/products/:id/` - Delete product
- POST `/api/products/vendor/bulk-upload/` - Bulk upload

**Shopping**:
- GET `/api/cart/` - Get cart
- POST `/api/cart/add/` - Add to cart
- PATCH `/api/cart/update/` - Update cart
- DELETE `/api/cart/remove/` - Remove from cart
- POST `/api/checkout/` - Checkout
- GET `/api/wishlist/` - List wishlist
- POST `/api/wishlist/` - Add to wishlist
- DELETE `/api/wishlist/:id/` - Remove from wishlist

**Orders**:
- GET `/api/orders/` - List orders
- GET `/api/orders/:id/` - Order details

**Vendors**:
- GET `/api/vendors/me/` - Vendor profile
- PATCH `/api/vendors/me/` - Update vendor
- GET `/api/vendors/me/payouts/` - List payouts
- POST `/api/vendors/me/payouts/` - Request payout

## 🚀 Getting Started

### Quick Setup

1. **Clone and setup**:
```bash
git clone https://github.com/franklineXonguti/Ecommerce-Web.git
cd Ecommerce-Web/backend
```

2. **Run setup script**:
```bash
# Linux/Mac
./setup.sh

# Windows
.\setup.ps1
```

3. **Access the application**:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Manual Setup

```bash
# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 📝 Usage Examples

### Complete Shopping Flow

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Register
response = requests.post(f"{BASE_URL}/auth/register/", json={
    "email": "customer@example.com",
    "password": "secure123",
    "password_confirm": "secure123",
    "first_name": "John",
    "last_name": "Doe"
})
token = response.json()['access']
headers = {"Authorization": f"Bearer {token}"}

# 2. Browse products
products = requests.get(f"{BASE_URL}/products/").json()

# 3. Add to cart
requests.post(f"{BASE_URL}/cart/add/", 
    headers=headers,
    json={"product_variant": 1, "quantity": 2}
)

# 4. View cart
cart = requests.get(f"{BASE_URL}/cart/", headers=headers).json()

# 5. Create address
address = requests.post(f"{BASE_URL}/account/addresses/",
    headers=headers,
    json={
        "street": "123 Main St",
        "city": "Nairobi",
        "county": "Nairobi",
        "postal_code": "00100",
        "phone_number": "+254712345678",
        "is_default": True
    }
).json()

# 6. Checkout
order = requests.post(f"{BASE_URL}/checkout/",
    headers=headers,
    json={"shipping_address": address['id']}
).json()

print(f"Order created: {order['order_number']}")
```

## 🐛 Known Issues

- Payment integration not yet implemented (coming in v0.2.0)
- Real-time stock updates via WebSocket need frontend testing
- Meilisearch integration is stubbed (coming in v0.3.0)
- AI recommendations not yet implemented (coming in v0.3.0)

## 🔜 What's Next (v0.2.0)

- Stripe payment integration
- M-Pesa STK Push integration
- Payment webhook handlers
- Stock reduction on payment
- Real-time stock WebSocket testing
- Inventory management improvements

See [BACKEND_ROADMAP.md](BACKEND_ROADMAP.md) for complete roadmap.

## 📚 Documentation

- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **API Reference**: [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)
- **Roadmap**: [BACKEND_ROADMAP.md](BACKEND_ROADMAP.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and submit pull requests.

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👏 Acknowledgments

Thanks to all contributors and the Django community!

---

**Version**: v0.1.0  
**Previous Version**: v0.0.1  
**Next Version**: v0.2.0 (Payments & Real-time)  
**Repository**: https://github.com/franklineXonguti/Ecommerce-Web
