from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/market/(?P<trading_pair_id>\w+)/$', consumers.MarketDataConsumer.as_asgi()),
    re_path(r'ws/orderbook/(?P<trading_pair_id>\w+)/$', consumers.OrderBookConsumer.as_asgi()),
    re_path(r'ws/trades/(?P<trading_pair_id>\w+)/$', consumers.TradesConsumer.as_asgi()),
]