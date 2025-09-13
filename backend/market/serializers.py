from rest_framework import serializers
from .models import MarketData, NewsArticle, MarketAlert, TechnicalIndicator
from trading.serializers import TradingPairSerializer, CryptocurrencySerializer

class MarketDataSerializer(serializers.ModelSerializer):
    """Serializer for market data"""
    
    trading_pair = TradingPairSerializer(read_only=True)
    
    class Meta:
        model = MarketData
        fields = [
            'trading_pair', 'last_price', 'bid_price', 'ask_price',
            'high_24h', 'low_24h', 'volume_24h', 'volume_24h_quote',
            'price_change_24h', 'price_change_percent_24h',
            'market_cap', 'circulating_supply', 'updated_at'
        ]


class NewsArticleSerializer(serializers.ModelSerializer):
    """Serializer for news articles"""
    
    related_cryptocurrencies = CryptocurrencySerializer(many=True, read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'title_en', 'content', 'summary',
            'related_cryptocurrencies', 'author', 'source', 'source_url',
            'category', 'tags', 'is_featured', 'published_at', 'created_at'
        ]


class NewsArticleListSerializer(serializers.ModelSerializer):
    """Simplified serializer for news article lists"""
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'summary', 'author', 'source',
            'category', 'is_featured', 'published_at'
        ]


class MarketAlertSerializer(serializers.ModelSerializer):
    """Serializer for market alerts"""
    
    trading_pair = TradingPairSerializer(read_only=True)
    trading_pair_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = MarketAlert
        fields = [
            'id', 'user', 'trading_pair', 'trading_pair_id', 'alert_type',
            'target_value', 'status', 'notify_email', 'notify_sms', 'notify_push',
            'expires_at', 'created_at', 'triggered_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'triggered_at']
    
    def validate(self, attrs):
        trading_pair_id = attrs.get('trading_pair_id')
        target_value = attrs.get('target_value')
        
        # Validate trading pair
        try:
            from trading.models import TradingPair
            trading_pair = TradingPair.objects.get(id=trading_pair_id, is_active=True)
            attrs['trading_pair'] = trading_pair
        except TradingPair.DoesNotExist:
            raise serializers.ValidationError("جفت معاملاتی نامعتبر است")
        
        # Validate target value
        if target_value <= 0:
            raise serializers.ValidationError("مقدار هدف باید مثبت باشد")
        
        return attrs


class CreateMarketAlertSerializer(serializers.Serializer):
    """Serializer for creating market alerts"""
    
    trading_pair_id = serializers.IntegerField()
    alert_type = serializers.ChoiceField(choices=MarketAlert.ALERT_TYPES)
    target_value = serializers.DecimalField(max_digits=20, decimal_places=8)
    notify_email = serializers.BooleanField(default=True)
    notify_sms = serializers.BooleanField(default=False)
    notify_push = serializers.BooleanField(default=True)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    
    def validate(self, attrs):
        trading_pair_id = attrs.get('trading_pair_id')
        target_value = attrs.get('target_value')
        
        # Validate trading pair
        try:
            from trading.models import TradingPair
            trading_pair = TradingPair.objects.get(id=trading_pair_id, is_active=True)
            attrs['trading_pair'] = trading_pair
        except TradingPair.DoesNotExist:
            raise serializers.ValidationError("جفت معاملاتی نامعتبر است")
        
        # Validate target value
        if target_value <= 0:
            raise serializers.ValidationError("مقدار هدف باید مثبت باشد")
        
        return attrs


class TechnicalIndicatorSerializer(serializers.ModelSerializer):
    """Serializer for technical indicators"""
    
    trading_pair = TradingPairSerializer(read_only=True)
    
    class Meta:
        model = TechnicalIndicator
        fields = [
            'trading_pair', 'indicator_type', 'timeframe', 'values',
            'signal', 'confidence', 'calculated_at'
        ]


class MarketOverviewSerializer(serializers.Serializer):
    """Serializer for market overview"""
    
    total_market_cap = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_volume_24h = serializers.DecimalField(max_digits=20, decimal_places=2)
    bitcoin_dominance = serializers.DecimalField(max_digits=5, decimal_places=2)
    active_cryptocurrencies = serializers.IntegerField()
    active_trading_pairs = serializers.IntegerField()
    top_gainers = MarketDataSerializer(many=True)
    top_losers = MarketDataSerializer(many=True)
    most_active = MarketDataSerializer(many=True)


class PriceAlertSummarySerializer(serializers.Serializer):
    """Serializer for price alert summary"""
    
    total_alerts = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    triggered_alerts = serializers.IntegerField()
    recent_alerts = MarketAlertSerializer(many=True)