from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/auth/', include('user_accounts.urls')),
    path('api/account/', include('user_accounts.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/products/', include('products.urls')),
    path('api/vendor/products/', include('products.urls')),
    path('api/cart/', include('orders.urls')),
    path('api/wishlist/', include('orders.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
