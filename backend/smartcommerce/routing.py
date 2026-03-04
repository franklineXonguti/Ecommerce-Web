from django.urls import re_path
from products.consumers import StockConsumer

websocket_urlpatterns = [
    re_path(r'ws/stock/(?P<product_id>\d+)/$', StockConsumer.as_asgi()),
]
