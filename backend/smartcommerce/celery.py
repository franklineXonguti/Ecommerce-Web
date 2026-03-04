import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcommerce.settings.development')

app = Celery('smartcommerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'check-abandoned-carts': {
        'task': 'notifications.tasks.process_abandoned_carts',
        'schedule': crontab(hour='*/6'),  # Every 6 hours
    },
    'update-analytics': {
        'task': 'analytics.tasks.update_daily_metrics',
        'schedule': crontab(hour=1, minute=0),  # Daily at 1 AM
    },
    'check-pending-mpesa-payments': {
        'task': 'payments.tasks.check_pending_mpesa_payments',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}
