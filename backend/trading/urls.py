from django.urls import path
from . import views

urlpatterns = [
    # Market data
    path('cryptocurrencies/', views.CryptocurrencyListView.as_view(), name='cryptocurrency_list'),
    path('pairs/', views.TradingPairListView.as_view(), name='trading_pair_list'),
    path('market-stats/', views.market_stats, name='market_stats'),
    
    # Orders
    path('orders/create/', views.CreateOrderView.as_view(), name='create_order'),
    path('orders/', views.UserOrdersView.as_view(), name='user_orders'),
    path('orders/<uuid:order_id>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
    
    # Trades
    path('trades/', views.UserTradesView.as_view(), name='user_trades'),
    path('trading-stats/', views.trading_stats, name='trading_stats'),
    
    # Market data for specific pairs
    path('pairs/<int:trading_pair_id>/orderbook/', views.OrderBookView.as_view(), name='order_book'),
    path('pairs/<int:trading_pair_id>/trades/', views.RecentTradesView.as_view(), name='recent_trades'),
    path('pairs/<int:trading_pair_id>/history/', views.PriceHistoryView.as_view(), name='price_history'),
]