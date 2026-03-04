# Payment Integration Testing Guide

Complete guide for testing Stripe and M-Pesa payment integrations.

## Prerequisites

### Stripe Setup
1. Create account at https://stripe.com
2. Get API keys from Dashboard → Developers → API keys
3. Get webhook secret from Dashboard → Developers → Webhooks

### M-Pesa Setup (Sandbox)
1. Register at https://developer.safaricom.co.ke
2. Create app to get Consumer Key and Consumer Secret
3. Get test credentials from Daraja API documentation

## Configuration

### Environment Variables

Add to `.env`:

```env
# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# M-Pesa (Sandbox)
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/payments/mpesa/callback/

# Frontend
FRONTEND_URL=http://localhost:3000
```

## Testing Stripe Payments

### 1. Create Order

```bash
# First, create an order via checkout
curl -X POST http://localhost:8000/api/checkout/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": 1
  }'
```

Response:
```json
{
  "id": 1,
  "order_number": "ORD-ABC123",
  "status": "PENDING_PAYMENT",
  "payment_status": "PENDING",
  "total_kes": "5000.00"
}
```

### 2. Create Stripe Checkout Session

```bash
curl -X POST http://localhost:8000/api/payments/stripe/create-checkout-session/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1
  }'
```

Response:
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_...",
  "session_id": "cs_test_..."
}
```

### 3. Complete Payment

- Open `checkout_url` in browser
- Use test card: `4242 4242 4242 4242`
- Any future expiry date
- Any 3-digit CVC
- Any billing details

### 4. Verify Payment

```bash
curl -X GET http://localhost:8000/api/payments/status/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
  "id": 1,
  "order_number": "ORD-ABC123",
  "provider": "STRIPE",
  "status": "SUCCESS",
  "amount_kes": "5000.00"
}
```

### Stripe Test Cards

| Card Number | Description |
|-------------|-------------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Declined |
| 4000 0025 0000 3155 | Requires authentication |
| 4000 0000 0000 0002 | Declined (generic) |

## Testing M-Pesa Payments

### 1. Create Order

Same as Stripe (see above)

### 2. Initiate STK Push

```bash
curl -X POST http://localhost:8000/api/payments/mpesa/stk-push/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "phone_number": "254712345678"
  }'
```

Response:
```json
{
  "message": "STK push sent successfully",
  "checkout_request_id": "ws_CO_...",
  "merchant_request_id": "..."
}
```

### 3. Complete Payment on Phone

- Check phone for M-Pesa prompt
- Enter M-Pesa PIN
- Confirm payment

### 4. Query Payment Status

```bash
curl -X POST http://localhost:8000/api/payments/mpesa/query-status/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "checkout_request_id": "ws_CO_..."
  }'
```

Response:
```json
{
  "status": "SUCCESS",
  "result": {
    "ResultCode": "0",
    "ResultDesc": "The service request is processed successfully."
  }
}
```

### M-Pesa Sandbox Test Numbers

For sandbox testing, use:
- Phone: `254708374149` (or any 254... number)
- PIN: Any 4 digits in sandbox

## Webhook Testing

### Stripe Webhook (Local Testing)

1. **Install Stripe CLI**:
```bash
# Mac
brew install stripe/stripe-cli/stripe

# Windows
scoop install stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.0/stripe_1.19.0_linux_x86_64.tar.gz
tar -xvf stripe_1.19.0_linux_x86_64.tar.gz
```

2. **Login to Stripe**:
```bash
stripe login
```

3. **Forward webhooks to local server**:
```bash
stripe listen --forward-to localhost:8000/api/payments/stripe/webhook/
```

4. **Get webhook secret** from output and add to `.env`:
```env
STRIPE_WEBHOOK_SECRET=whsec_...
```

5. **Trigger test webhook**:
```bash
stripe trigger checkout.session.completed
```

### M-Pesa Webhook (Local Testing)

For local testing, you need a public URL. Use ngrok:

1. **Install ngrok**:
```bash
# Download from https://ngrok.com/download
```

2. **Start ngrok**:
```bash
ngrok http 8000
```

3. **Update callback URL** in `.env`:
```env
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok.io/api/payments/mpesa/callback/
```

4. **Test callback** with curl:
```bash
curl -X POST https://your-ngrok-url.ngrok.io/api/payments/mpesa/callback/ \
  -H "Content-Type: application/json" \
  -d '{
    "Body": {
      "stkCallback": {
        "ResultCode": 0,
        "CheckoutRequestID": "ws_CO_...",
        "CallbackMetadata": {
          "Item": [
            {"Name": "MpesaReceiptNumber", "Value": "ABC123"}
          ]
        }
      }
    }
  }'
```

## Testing Payment Flows

### Complete Stripe Flow

```python
import requests

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_jwt_token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# 1. Add items to cart
requests.post(f"{BASE_URL}/cart/add/", 
    headers=headers,
    json={"product_variant": 1, "quantity": 2}
)

# 2. Create address
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

# 3. Checkout
order = requests.post(f"{BASE_URL}/checkout/",
    headers=headers,
    json={"shipping_address": address['id']}
).json()

# 4. Create Stripe session
payment = requests.post(f"{BASE_URL}/payments/stripe/create-checkout-session/",
    headers=headers,
    json={"order_id": order['id']}
).json()

print(f"Complete payment at: {payment['checkout_url']}")

# 5. Check status (after payment)
status = requests.get(f"{BASE_URL}/payments/status/1/", headers=headers).json()
print(f"Payment status: {status['status']}")
```

### Complete M-Pesa Flow

```python
import requests
import time

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_jwt_token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# 1-3. Same as Stripe (cart, address, checkout)

# 4. Initiate STK Push
payment = requests.post(f"{BASE_URL}/payments/mpesa/stk-push/",
    headers=headers,
    json={
        "order_id": order['id'],
        "phone_number": "254712345678"
    }
).json()

checkout_request_id = payment['checkout_request_id']
print(f"Check your phone for M-Pesa prompt")

# 5. Wait and query status
time.sleep(30)  # Wait for user to complete payment

status = requests.post(f"{BASE_URL}/payments/mpesa/query-status/",
    headers=headers,
    json={"checkout_request_id": checkout_request_id}
).json()

print(f"Payment status: {status['status']}")
```

## Troubleshooting

### Stripe Issues

**Issue**: Webhook not receiving events
- **Solution**: Check Stripe CLI is running and forwarding
- Verify webhook secret in `.env`
- Check Django logs: `docker-compose logs -f web`

**Issue**: Payment not completing
- **Solution**: Check test card number
- Verify Stripe API keys are correct
- Check order status is PENDING_PAYMENT

### M-Pesa Issues

**Issue**: STK Push not received
- **Solution**: Verify phone number format (254XXXXXXXXX)
- Check M-Pesa credentials in `.env`
- Ensure callback URL is publicly accessible

**Issue**: Callback not working
- **Solution**: Use ngrok for local testing
- Verify callback URL in Daraja portal
- Check Django logs for callback data

**Issue**: "Invalid Access Token"
- **Solution**: Verify Consumer Key and Secret
- Check if credentials are for sandbox/production
- Regenerate access token

## Production Checklist

### Stripe
- [ ] Switch to live API keys
- [ ] Configure production webhook endpoint
- [ ] Add webhook endpoint to Stripe dashboard
- [ ] Test with real cards (small amounts)
- [ ] Enable 3D Secure authentication
- [ ] Set up Stripe Radar for fraud detection

### M-Pesa
- [ ] Get production credentials from Safaricom
- [ ] Update MPESA_CALLBACK_URL to production domain
- [ ] Change base URL in MPesaService to production
- [ ] Test with real phone numbers
- [ ] Set up monitoring for failed transactions
- [ ] Configure automatic reconciliation

### General
- [ ] Enable HTTPS for all payment endpoints
- [ ] Set up payment failure notifications
- [ ] Configure automatic refund handling
- [ ] Add payment analytics tracking
- [ ] Set up backup payment logs
- [ ] Test error scenarios
- [ ] Document payment flows for support team

## Monitoring

### Check Payment Status

```bash
# View recent payments
docker-compose exec web python manage.py shell
>>> from payments.models import Payment
>>> Payment.objects.order_by('-created_at')[:10]
```

### Check Celery Tasks

```bash
# View Celery logs
docker-compose logs -f celery-worker

# Check pending M-Pesa payments task
docker-compose exec celery-worker celery -A smartcommerce inspect active
```

### Database Queries

```sql
-- Payments by status
SELECT status, COUNT(*) FROM payments_payment GROUP BY status;

-- Failed payments
SELECT * FROM payments_payment WHERE status = 'FAILED' ORDER BY created_at DESC;

-- Revenue by provider
SELECT provider, SUM(amount_kes) FROM payments_payment 
WHERE status = 'SUCCESS' GROUP BY provider;
```

## Support

For issues:
1. Check Django logs: `docker-compose logs -f web`
2. Check Celery logs: `docker-compose logs -f celery-worker`
3. Review payment model: `Payment.objects.filter(order_id=X)`
4. Check Stripe dashboard for payment details
5. Review M-Pesa transaction logs in Daraja portal

---

**Last Updated**: v0.2.0
**Status**: Payment integration complete
