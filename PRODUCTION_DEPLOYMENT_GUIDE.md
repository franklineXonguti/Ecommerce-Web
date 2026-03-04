# Production Deployment Guide

Complete guide for deploying SmartCommerce to production.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Application Deployment](#application-deployment)
5. [Service Configuration](#service-configuration)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup Strategy](#backup-strategy)
9. [Scaling Considerations](#scaling-considerations)

---

## Pre-Deployment Checklist

### Code Preparation
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] No debug statements or print() calls
- [ ] All TODO comments addressed
- [ ] Dependencies locked (requirements.txt)
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Static files collected
- [ ] Media upload tested

### Infrastructure
- [ ] Domain name registered
- [ ] SSL certificate obtained
- [ ] CDN configured (optional)
- [ ] Email service configured
- [ ] Payment gateways in production mode
- [ ] Monitoring tools set up
- [ ] Backup system configured

### Security
- [ ] SECRET_KEY changed from default
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configured
- [ ] CORS settings reviewed
- [ ] Rate limiting enabled
- [ ] SQL injection prevention verified
- [ ] XSS protection enabled
- [ ] CSRF protection enabled

---

## Environment Setup

### 1. Server Requirements

**Minimum Specifications**:
- CPU: 2 cores
- RAM: 4GB
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS

**Recommended Specifications**:
- CPU: 4 cores
- RAM: 8GB
- Storage: 100GB SSD
- OS: Ubuntu 22.04 LTS

### 2. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y

# Install Supervisor (for process management)
sudo apt install supervisor -y

# Install certbot (for SSL)
sudo apt install certbot python3-certbot-nginx -y
```

### 3. Create Application User

```bash
sudo adduser smartcommerce
sudo usermod -aG sudo smartcommerce
su - smartcommerce
```

### 4. Clone Repository

```bash
cd /home/smartcommerce
git clone https://github.com/franklineXonguti/Ecommerce-Web.git
cd Ecommerce-Web/backend
```

### 5. Setup Python Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements/production.txt
```

---

## Database Setup

### 1. Create PostgreSQL Database

```bash
sudo -u postgres psql

CREATE DATABASE smartcommerce_prod;
CREATE USER smartcommerce_user WITH PASSWORD 'your_secure_password';
ALTER ROLE smartcommerce_user SET client_encoding TO 'utf8';
ALTER ROLE smartcommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE smartcommerce_user SET timezone TO 'Africa/Nairobi';
GRANT ALL PRIVILEGES ON DATABASE smartcommerce_prod TO smartcommerce_user;
\q
```

### 2. Configure Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup_db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/smartcommerce/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="smartcommerce_prod"

mkdir -p $BACKUP_DIR
pg_dump -U smartcommerce_user $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup_db.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /usr/local/bin/backup_db.sh
```

---

## Application Deployment

### 1. Environment Variables

Create production `.env`:

```bash
nano /home/smartcommerce/Ecommerce-Web/backend/.env
```

```env
# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=smartcommerce_prod
DB_USER=smartcommerce_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Channels
CHANNEL_LAYERS_HOST=redis://localhost:6379/1

# Meilisearch
MEILISEARCH_HOST=http://localhost:7700
MEILISEARCH_API_KEY=your_production_master_key

# Stripe (Production)
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# M-Pesa (Production)
MPESA_CONSUMER_KEY=your_production_key
MPESA_CONSUMER_SECRET=your_production_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_production_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/payments/mpesa/callback/

# Email (Production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=SmartCommerce <noreply@yourdomain.com>

# Frontend
FRONTEND_URL=https://yourdomain.com

# Sentry (Optional)
SENTRY_DSN=https://...@sentry.io/...

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Run Migrations

```bash
cd /home/smartcommerce/Ecommerce-Web/backend
source venv/bin/activate
python manage.py migrate --settings=smartcommerce.settings.production
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput --settings=smartcommerce.settings.production
```

### 4. Create Superuser

```bash
python manage.py createsuperuser --settings=smartcommerce.settings.production
```

### 5. Configure Search Index

```bash
python manage.py configure_search --settings=smartcommerce.settings.production
python manage.py reindex_products --settings=smartcommerce.settings.production
```

---

## Service Configuration

### 1. Gunicorn Configuration

Create Gunicorn config:

```bash
nano /home/smartcommerce/Ecommerce-Web/backend/gunicorn_config.py
```

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/home/smartcommerce/logs/gunicorn_access.log"
errorlog = "/home/smartcommerce/logs/gunicorn_error.log"
loglevel = "info"
```

### 2. Supervisor Configuration

Create supervisor configs:

```bash
sudo nano /etc/supervisor/conf.d/smartcommerce.conf
```

```ini
[program:smartcommerce_web]
command=/home/smartcommerce/Ecommerce-Web/backend/venv/bin/gunicorn smartcommerce.wsgi:application -c /home/smartcommerce/Ecommerce-Web/backend/gunicorn_config.py
directory=/home/smartcommerce/Ecommerce-Web/backend
user=smartcommerce
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/smartcommerce/logs/web.log

[program:smartcommerce_celery]
command=/home/smartcommerce/Ecommerce-Web/backend/venv/bin/celery -A smartcommerce worker -l info
directory=/home/smartcommerce/Ecommerce-Web/backend
user=smartcommerce
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/smartcommerce/logs/celery.log

[program:smartcommerce_celery_beat]
command=/home/smartcommerce/Ecommerce-Web/backend/venv/bin/celery -A smartcommerce beat -l info
directory=/home/smartcommerce/Ecommerce-Web/backend
user=smartcommerce
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/smartcommerce/logs/celery_beat.log

[program:smartcommerce_daphne]
command=/home/smartcommerce/Ecommerce-Web/backend/venv/bin/daphne -b 127.0.0.1 -p 8001 smartcommerce.asgi:application
directory=/home/smartcommerce/Ecommerce-Web/backend
user=smartcommerce
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/smartcommerce/logs/daphne.log
```

```bash
# Create log directory
mkdir -p /home/smartcommerce/logs

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### 3. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/smartcommerce
```

```nginx
upstream smartcommerce_web {
    server 127.0.0.1:8000;
}

upstream smartcommerce_ws {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 100M;
    
    # Static files
    location /static/ {
        alias /home/smartcommerce/Ecommerce-Web/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /home/smartcommerce/Ecommerce-Web/backend/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    # WebSocket
    location /ws/ {
        proxy_pass http://smartcommerce_ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API
    location / {
        proxy_pass http://smartcommerce_web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/smartcommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Security Hardening

### 1. Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. PostgreSQL Security

```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Change:
```
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
```

### 4. Redis Security

```bash
sudo nano /etc/redis/redis.conf
```

Add:
```
bind 127.0.0.1
requirepass your_redis_password
```

---

## Monitoring & Logging

### 1. Setup Sentry

Already configured in production settings if SENTRY_DSN is set.

### 2. Log Rotation

```bash
sudo nano /etc/logrotate.d/smartcommerce
```

```
/home/smartcommerce/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 smartcommerce smartcommerce
    sharedscripts
    postrotate
        supervisorctl restart smartcommerce_web smartcommerce_celery smartcommerce_celery_beat smartcommerce_daphne
    endscript
}
```

### 3. Health Check Endpoint

Add to Django:

```python
# In smartcommerce/urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
    # ... other patterns
]
```

---

## Backup Strategy

### 1. Database Backups
- Automated daily backups (configured above)
- Weekly full backups to external storage
- Monthly archives

### 2. Media Files Backup

```bash
# Create backup script
nano /usr/local/bin/backup_media.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/smartcommerce/backups/media"
DATE=$(date +%Y%m%d)
MEDIA_DIR="/home/smartcommerce/Ecommerce-Web/backend/media"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz $MEDIA_DIR

# Keep only last 30 days
find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime +30 -delete
```

### 3. Offsite Backups

Use AWS S3, Google Cloud Storage, or similar:

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Sync backups
aws s3 sync /home/smartcommerce/backups s3://your-bucket/backups/
```

---

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or HAProxy
2. **Multiple App Servers**: Run multiple Gunicorn instances
3. **Separate Celery Workers**: Dedicated servers for background tasks
4. **Database Replication**: Master-slave PostgreSQL setup
5. **Redis Cluster**: For high availability

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Add database indexes
4. Enable query caching
5. Use CDN for static/media files

### Performance Optimization

1. **Database**:
   - Connection pooling
   - Query optimization
   - Proper indexing

2. **Caching**:
   - Redis for session storage
   - Cache frequently accessed data
   - Use Django's cache framework

3. **Static Files**:
   - Use CDN (CloudFlare, AWS CloudFront)
   - Enable gzip compression
   - Set proper cache headers

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check services
sudo supervisorctl status

# Check logs
tail -f /home/smartcommerce/logs/web.log
tail -f /home/smartcommerce/logs/celery.log

# Test API
curl https://yourdomain.com/health/
curl https://yourdomain.com/api/products/
```

### 2. Monitor Performance

- Set up uptime monitoring (UptimeRobot, Pingdom)
- Configure error tracking (Sentry)
- Monitor server resources (htop, netdata)
- Track application metrics

### 3. Regular Maintenance

- Weekly: Review logs for errors
- Monthly: Update dependencies
- Quarterly: Security audit
- Annually: Infrastructure review

---

## Troubleshooting

### Common Issues

**502 Bad Gateway**:
- Check Gunicorn is running: `sudo supervisorctl status`
- Check logs: `tail -f /home/smartcommerce/logs/web.log`

**Database Connection Error**:
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in `.env`

**Static Files Not Loading**:
- Run collectstatic again
- Check Nginx configuration
- Verify file permissions

**Celery Tasks Not Running**:
- Check Celery worker: `sudo supervisorctl status smartcommerce_celery`
- Check Redis: `redis-cli ping`

---

## Support

For deployment issues:
1. Check logs in `/home/smartcommerce/logs/`
2. Review Django error pages (if DEBUG=True temporarily)
3. Check Sentry for error tracking
4. Review GitHub Issues

---

**Deployment Checklist Complete** ✅

Your SmartCommerce backend is now production-ready!
