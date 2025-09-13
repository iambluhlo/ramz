from django.urls import path
from . import views

urlpatterns = [
    # Market data
    path('data/', views.MarketDataListView.as_view(), name='market_data_list'),
    path('data/<int:trading_pair_id>/', views.MarketDataDetailView.as_view(), name='market_data_detail'),
    path('overview/', views.market_overview, name='market_overview'),
    path('sentiment/', views.market_sentiment, name='market_sentiment'),
    
    # News
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/trending/', views.trending_news, name='trending_news'),
    
    # Alerts
    path('alerts/', views.UserMarketAlertsView.as_view(), name='user_market_alerts'),
    path('alerts/<int:alert_id>/cancel/', views.CancelMarketAlertView.as_view(), name='cancel_market_alert'),
    path('alerts/summary/', views.alert_summary, name='alert_summary'),
    
    # Technical analysis
    path('indicators/<int:trading_pair_id>/', views.TechnicalIndicatorsView.as_view(), name='technical_indicators'),
]