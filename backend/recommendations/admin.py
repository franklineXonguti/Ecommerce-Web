from django.contrib import admin
from .models import UserProductEvent


@admin.register(UserProductEvent)
class UserProductEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'event_type', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user__email', 'product__name']
