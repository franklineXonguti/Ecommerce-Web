# SmartCommerce API Documentation

Complete API reference for frontend integration.

## Base URL
```
Development: http://localhost:8000/api/
Production: https://api.yourdomain.com/api/
```

## Authentication

All authenticated endpoints require JWT token in header:
```
Authorization: Bearer <access_token>
```

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678"
}

Response 201:
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+254712345678",
    "is_vendor": false,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## User Profile

### Get Profile
```http
GET /api/account/profile/
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "is_vendor": false,
  "business_name": "",
  "business_registration_number": "",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Update Profile
```http
PATCH /api/account/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Jane",
  "phone_number": "+254798765432"
}

Response 200: (same as GET)
```

## Addresses

### List Addresses
```http
GET /api/account/addresses/
Authorization: Bearer <token>

Response 200:
[
  {
    "id": 1,
    "street": "123 Main St",
    "city": "Nairobi",
    "county": "Nairobi",
    "postal_code": "00100",
    "phone_number": "+254712345678",
    "is_default": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Address
```http
POST /api/account/addresses/
Authorization: Bearer <token>
Content-Type: application/json

{
  "street": "456 Oak Ave",
  "city": "Mombasa",
  "county": "Mombasa",
  "postal_code": "80100",
  "phone_number": "+254712345678",
  "is_default": false
}

Response 201: (address object)
```

## Products

### List Products
```http
GET /api/products/?category=1&search=laptop&ordering=-created_at&page=1
Authorization: Not required

Query Parameters:
- category: Filter by category ID
- vendor: Filter by vendor ID
- search: Search in name and description
- ordering: Sort by price_kes, -price_kes, created_at, -created_at
- page: Page number (20 items per page)

Response 200:
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "MacBook Pro",
      "slug": "macbook-pro",
      "price_kes": "150000.00",
      "category_name": "Laptops",
      "primary_image": "http://localhost:8000/media/products/macbook.jpg",
      "is_active": true
    }
  ]
}
```

### Product Details
```http
GET /api/products/1/
Authorization: Not required

Response 200:
{
  "id": 1,
  "name": "MacBook Pro",
  "slug": "macbook-pro",
  "description": "Powerful laptop for professionals",
  "price_kes": "150000.00",
  "category": {
    "id": 1,
    "name": "Laptops",
    "slug": "laptops",
    "parent": null
  },
  "vendor_name": "Tech Store",
  "variants": [
    {
      "id": 1,
      "sku": "MBP-13-256",
      "size": "13 inch",
      "color": "Space Gray",
      "price": "150000.00",
      "stock": 5
    }
  ],
  "images": [
    {
      "id": 1,
      "image": "http://localhost:8000/media/products/macbook.jpg",
      "is_primary": true
    }
  ],
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Cart

### Get Cart
```http
GET /api/cart/
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "status": "ACTIVE",
  "items": [
    {
      "id": 1,
      "product_variant": 1,
      "product_name": "MacBook Pro",
      "quantity": 2,
      "price": "150000.00"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Wishlist

### Get Wishlist
```http
GET /api/wishlist/
Authorization: Bearer <token>

Response 200:
[
  {
    "id": 1,
    "product": 1,
    "product_name": "MacBook Pro",
    "product_price": "150000.00",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Add to Wishlist
```http
POST /api/wishlist/
Authorization: Bearer <token>
Content-Type: application/json

{
  "product": 1
}

Response 201: (wishlist item object)
```

## Orders

### List Orders
```http
GET /api/orders/
Authorization: Bearer <token>

Response 200:
[
  {
    "id": 1,
    "order_number": "ORD-ABC123DEF456",
    "status": "PAID",
    "payment_status": "PAID",
    "total_kes": "300000.00",
    "shipping_address": 1,
    "billing_address": 1,
    "items": [
      {
        "id": 1,
        "product_variant": 1,
        "quantity": 2,
        "unit_price_kes": "150000.00",
        "subtotal_kes": "300000.00"
      }
    ],
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Order Details
```http
GET /api/orders/1/
Authorization: Bearer <token>

Response 200: (same as list item)
```

## Search

### Search Products
```http
GET /api/search/products/?q=laptop&category=1&price_min=50000&price_max=200000
Authorization: Not required

Query Parameters:
- q: Search query
- category: Filter by category
- price_min: Minimum price in KES
- price_max: Maximum price in KES

Response 200:
{
  "results": [],
  "total": 0
}
```

## Recommendations

### User Recommendations
```http
GET /api/recommendations/for-user/
Authorization: Bearer <token>

Response 200:
{
  "products": [1, 5, 12, 23]
}
```

### Product Recommendations
```http
GET /api/recommendations/for-product/1/
Authorization: Not required

Response 200:
{
  "products": [2, 3, 7, 15]
}
```

## Payments

### Create Stripe Checkout
```http
POST /api/payments/stripe/create-checkout-session/
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": 1
}

Response 200:
{
  "checkout_url": "https://checkout.stripe.com/..."
}
```

### M-Pesa STK Push
```http
POST /api/payments/mpesa/stk-push/
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": 1,
  "phone_number": "254712345678"
}

Response 200:
{
  "message": "STK push sent",
  "checkout_request_id": "ws_CO_..."
}
```

## Vendors

### Get Vendor Profile
```http
GET /api/vendors/me/
Authorization: Bearer <token> (vendor only)

Response 200:
{
  "id": 1,
  "display_name": "Tech Store",
  "slug": "tech-store",
  "description": "Best tech products",
  "is_approved": true,
  "commission_rate": "10.00",
  "owner_email": "vendor@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Vendor Payouts
```http
GET /api/vendors/me/payouts/
Authorization: Bearer <token> (vendor only)

Response 200:
[
  {
    "id": 1,
    "vendor": 1,
    "vendor_name": "Tech Store",
    "amount_kes": "50000.00",
    "status": "PENDING",
    "reference": "",
    "requested_at": "2024-01-01T00:00:00Z",
    "processed_at": null,
    "notes": ""
  }
]
```

## Analytics

### Admin Analytics
```http
GET /api/analytics/admin/summary/
Authorization: Bearer <token> (admin only)

Response 200:
{
  "daily_revenue": [],
  "top_products": [],
  "customer_growth": [],
  "orders_by_status": {}
}
```

### Vendor Analytics
```http
GET /api/analytics/vendor/summary/
Authorization: Bearer <token> (vendor only)

Response 200:
{
  "revenue_by_day": [],
  "best_selling_products": [],
  "pending_payouts": 0
}
```

## WebSocket

### Stock Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stock/1/');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Stock update:', data);
  // { product_id: 1, stock: 7 }
};
```

## Error Responses

All endpoints may return these error codes:

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```
