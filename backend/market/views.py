from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, Max, Min
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import MarketData, NewsArticle, MarketAlert, TechnicalIndicator
from .serializers import (
    MarketDataSerializer, NewsArticleSerializer, NewsArticleListSerializer,
    MarketAlertSerializer, CreateMarketAlertSerializer, TechnicalIndicatorSerializer,
    MarketOverviewSerializer, PriceAlertSummarySerializer
)
from trading.models import TradingPair, Cryptocurrency

class MarketDataListView(generics.ListAPIView):
    """List market data for all trading pairs"""
    
    queryset = MarketData.objects.all().select_related(
        'trading_pair__base_currency', 'trading_pair__quote_currency'
    )
    serializer_class = MarketDataSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by base currency
        base_currency = self.request.query_params.get('base_currency')
        if base_currency:
            queryset = queryset.filter(trading_pair__base_currency__symbol=base_currency)
        
        # Filter by quote currency
        quote_currency = self.request.query_params.get('quote_currency')
        if quote_currency:
            queryset = queryset.filter(trading_pair__quote_currency__symbol=quote_currency)
        
        # Sort by volume or price change
        sort_by = self.request.query_params.get('sort_by', 'volume_24h')
        if sort_by in ['volume_24h', 'price_change_percent_24h', 'last_price']:
            queryset = queryset.order_by(f'-{sort_by}')
        
        return queryset


class MarketDataDetailView(generics.RetrieveAPIView):
    """Get market data for a specific trading pair"""
    
    serializer_class = MarketDataSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'trading_pair_id'
    
    def get_object(self):
        trading_pair_id = self.kwargs.get('trading_pair_id')
        try:
            return MarketData.objects.select_related(
                'trading_pair__base_currency', 'trading_pair__quote_currency'
            ).get(trading_pair_id=trading_pair_id)
        except MarketData.DoesNotExist:
            # Create market data if it doesn't exist
            trading_pair = TradingPair.objects.get(id=trading_pair_id)
            return MarketData.objects.create(
                trading_pair=trading_pair,
                last_price=Decimal('0'),
                bid_price=Decimal('0'),
                ask_price=Decimal('0'),
                high_24h=Decimal('0'),
                low_24h=Decimal('0'),
                volume_24h=Decimal('0'),
                volume_24h_quote=Decimal('0'),
                price_change_24h=Decimal('0'),
                price_change_percent_24h=Decimal('0')
            )


class NewsListView(generics.ListAPIView):
    """List published news articles"""
    
    serializer_class = NewsArticleListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = NewsArticle.objects.filter(is_published=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by cryptocurrency
        crypto = self.request.query_params.get('cryptocurrency')
        if crypto:
            queryset = queryset.filter(related_cryptocurrencies__symbol=crypto)
        
        # Featured articles first
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-is_featured', '-published_at')


class NewsDetailView(generics.RetrieveAPIView):
    """Get news article detail"""
    
    queryset = NewsArticle.objects.filter(is_published=True)
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.AllowAny]


class UserMarketAlertsView(generics.ListCreateAPIView):
    """List and create user's market alerts"""
    
    serializer_class = MarketAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = MarketAlert.objects.filter(user=self.request.user).select_related(
            'trading_pair__base_currency', 'trading_pair__quote_currency'
        )
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by trading pair
        pair_filter = self.request.query_params.get('trading_pair')
        if pair_filter:
            queryset = queryset.filter(trading_pair_id=pair_filter)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMarketAlertSerializer
        return MarketAlertSerializer
    
    def perform_create(self, serializer):
        # Check alert limit per user
        user_alerts_count = MarketAlert.objects.filter(
            user=self.request.user,
            status='active'
        ).count()
        
        if user_alerts_count >= 50:  # Limit to 50 active alerts per user
            raise serializers.ValidationError("حداکثر تعداد هشدارهای فعال به پایان رسیده است")
        
        serializer.save(user=self.request.user)


class CancelMarketAlertView(generics.UpdateAPIView):
    """Cancel a market alert"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, alert_id):
        try:
            alert = MarketAlert.objects.get(id=alert_id, user=request.user)
        except MarketAlert.DoesNotExist:
            return Response(
                {'error': 'هشدار یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if alert.status != 'active':
            return Response(
                {'error': 'این هشدار قابل لغو نیست'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alert.status = 'cancelled'
        alert.save()
        
        return Response(
            MarketAlertSerializer(alert).data,
            status=status.HTTP_200_OK
        )


class TechnicalIndicatorsView(generics.ListAPIView):
    """Get technical indicators for a trading pair"""
    
    serializer_class = TechnicalIndicatorSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        trading_pair_id = self.kwargs.get('trading_pair_id')
        queryset = TechnicalIndicator.objects.filter(
            trading_pair_id=trading_pair_id
        ).select_related('trading_pair__base_currency', 'trading_pair__quote_currency')
        
        # Filter by timeframe
        timeframe = self.request.query_params.get('timeframe')
        if timeframe:
            queryset = queryset.filter(timeframe=timeframe)
        
        # Filter by indicator type
        indicator_type = self.request.query_params.get('indicator_type')
        if indicator_type:
            queryset = queryset.filter(indicator_type=indicator_type)
        
        return queryset.order_by('indicator_type', 'timeframe')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def market_overview(request):
    """Get market overview statistics"""
    
    # Get all market data
    market_data = MarketData.objects.select_related(
        'trading_pair__base_currency', 'trading_pair__quote_currency'
    )
    
    # Calculate totals
    total_market_cap = market_data.aggregate(
        total=Sum('market_cap')
    )['total'] or Decimal('0')
    
    total_volume_24h = market_data.aggregate(
        total=Sum('volume_24h_quote')
    )['total'] or Decimal('0')
    
    # Bitcoin dominance (simplified)
    btc_market_cap = market_data.filter(
        trading_pair__base_currency__symbol='BTC'
    ).aggregate(total=Sum('market_cap'))['total'] or Decimal('0')
    
    bitcoin_dominance = (btc_market_cap / total_market_cap * 100) if total_market_cap > 0 else Decimal('0')
    
    # Active counts
    active_cryptocurrencies = Cryptocurrency.objects.filter(is_active=True).count()
    active_trading_pairs = TradingPair.objects.filter(is_active=True).count()
    
    # Top performers
    top_gainers = market_data.filter(
        price_change_percent_24h__gt=0
    ).order_by('-price_change_percent_24h')[:5]
    
    top_losers = market_data.filter(
        price_change_percent_24h__lt=0
    ).order_by('price_change_percent_24h')[:5]
    
    most_active = market_data.order_by('-volume_24h')[:5]
    
    data = {
        'total_market_cap': total_market_cap,
        'total_volume_24h': total_volume_24h,
        'bitcoin_dominance': bitcoin_dominance,
        'active_cryptocurrencies': active_cryptocurrencies,
        'active_trading_pairs': active_trading_pairs,
        'top_gainers': MarketDataSerializer(top_gainers, many=True).data,
        'top_losers': MarketDataSerializer(top_losers, many=True).data,
        'most_active': MarketDataSerializer(most_active, many=True).data,
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def alert_summary(request):
    """Get user's alert summary"""
    
    user = request.user
    alerts = MarketAlert.objects.filter(user=user)
    
    total_alerts = alerts.count()
    active_alerts = alerts.filter(status='active').count()
    triggered_alerts = alerts.filter(status='triggered').count()
    
    # Recent alerts (last 10)
    recent_alerts = alerts.select_related(
        'trading_pair__base_currency', 'trading_pair__quote_currency'
    ).order_by('-created_at')[:10]
    
    data = {
        'total_alerts': total_alerts,
        'active_alerts': active_alerts,
        'triggered_alerts': triggered_alerts,
        'recent_alerts': MarketAlertSerializer(recent_alerts, many=True).data,
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trending_news(request):
    """Get trending news articles"""
    
    # Get featured and recent articles
    featured_articles = NewsArticle.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('-published_at')[:3]
    
    recent_articles = NewsArticle.objects.filter(
        is_published=True,
        published_at__gte=timezone.now() - timedelta(days=7)
    ).order_by('-published_at')[:10]
    
    return Response({
        'featured': NewsArticleListSerializer(featured_articles, many=True).data,
        'recent': NewsArticleListSerializer(recent_articles, many=True).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def market_sentiment(request):
    """Get market sentiment indicators"""
    
    # Calculate sentiment based on price changes
    market_data = MarketData.objects.all()
    
    total_pairs = market_data.count()
    if total_pairs == 0:
        return Response({
            'sentiment': 'neutral',
            'sentiment_score': 0,
            'bullish_pairs': 0,
            'bearish_pairs': 0,
            'neutral_pairs': 0,
        })
    
    bullish_pairs = market_data.filter(price_change_percent_24h__gt=2).count()
    bearish_pairs = market_data.filter(price_change_percent_24h__lt=-2).count()
    neutral_pairs = total_pairs - bullish_pairs - bearish_pairs
    
    # Calculate sentiment score (-100 to 100)
    sentiment_score = ((bullish_pairs - bearish_pairs) / total_pairs) * 100
    
    if sentiment_score > 20:
        sentiment = 'bullish'
    elif sentiment_score < -20:
        sentiment = 'bearish'
    else:
        sentiment = 'neutral'
    
    return Response({
        'sentiment': sentiment,
        'sentiment_score': round(sentiment_score, 2),
        'bullish_pairs': bullish_pairs,
        'bearish_pairs': bearish_pairs,
        'neutral_pairs': neutral_pairs,
        'total_pairs': total_pairs,
    })