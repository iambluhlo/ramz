from rest_framework import serializers
from decimal import Decimal
from .models import Cryptocurrency, TradingPair, Order, Trade, OrderBook, PriceHistory

class CryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for cryptocurrency"""
    
    class Meta:
        model = Cryptocurrency
        fields = [
            'id', 'symbol', 'name', 'name_fa', 'is_active',
            'min_trade_amount', 'max_trade_amount', 'maker_fee', 'taker_fee',
            'network', 'decimals'
        ]


class TradingPairSerializer(serializers.ModelSerializer):
    """Serializer for trading pairs"""
    
    base_currency = CryptocurrencySerializer(read_only=True)
    quote_currency = CryptocurrencySerializer(read_only=True)
    
    class Meta:
        model = TradingPair
        fields = [
            'id', 'symbol', 'base_currency', 'quote_currency', 'is_active',
            'min_price', 'max_price', 'price_precision', 'quantity_precision'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders"""
    
    trading_pair = TradingPairSerializer(read_only=True)
    trading_pair_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'trading_pair', 'trading_pair_id', 'order_type', 'side',
            'status', 'quantity', 'price', 'stop_price', 'filled_quantity',
            'remaining_quantity', 'fee', 'created_at', 'updated_at', 'executed_at'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'filled_quantity', 'remaining_quantity',
            'fee', 'created_at', 'updated_at', 'executed_at'
        ]
    
    def validate(self, attrs):
        trading_pair_id = attrs.get('trading_pair_id')
        order_type = attrs.get('order_type')
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        
        # Validate trading pair
        try:
            trading_pair = TradingPair.objects.get(id=trading_pair_id, is_active=True)
            attrs['trading_pair'] = trading_pair
        except TradingPair.DoesNotExist:
            raise serializers.ValidationError("جفت معاملاتی نامعتبر است")
        
        # Validate price for limit orders
        if order_type in ['limit', 'stop_limit'] and not price:
            raise serializers.ValidationError("قیمت برای سفارش محدود الزامی است")
        
        # Validate quantity
        if quantity <= 0:
            raise serializers.ValidationError("مقدار باید مثبت باشد")
        
        if quantity < trading_pair.base_currency.min_trade_amount:
            raise serializers.ValidationError(
                f"مقدار نمی‌تواند کمتر از {trading_pair.base_currency.min_trade_amount} باشد"
            )
        
        return attrs


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders"""
    
    trading_pair_id = serializers.IntegerField()
    order_type = serializers.ChoiceField(choices=Order.ORDER_TYPES)
    side = serializers.ChoiceField(choices=Order.ORDER_SIDES)
    quantity = serializers.DecimalField(max_digits=20, decimal_places=8)
    price = serializers.DecimalField(max_digits=20, decimal_places=8, required=False, allow_null=True)
    stop_price = serializers.DecimalField(max_digits=20, decimal_places=8, required=False, allow_null=True)
    
    def validate(self, attrs):
        # Same validation as OrderSerializer
        trading_pair_id = attrs.get('trading_pair_id')
        order_type = attrs.get('order_type')
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        
        try:
            trading_pair = TradingPair.objects.get(id=trading_pair_id, is_active=True)
            attrs['trading_pair'] = trading_pair
        except TradingPair.DoesNotExist:
            raise serializers.ValidationError("جفت معاملاتی نامعتبر است")
        
        if order_type in ['limit', 'stop_limit'] and not price:
            raise serializers.ValidationError("قیمت برای سفارش محدود الزامی است")
        
        if quantity <= 0:
            raise serializers.ValidationError("مقدار باید مثبت باشد")
        
        if quantity < trading_pair.base_currency.min_trade_amount:
            raise serializers.ValidationError(
                f"مقدار نمی‌تواند کمتر از {trading_pair.base_currency.min_trade_amount} باشد"
            )
        
        return attrs


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for trades"""
    
    trading_pair = TradingPairSerializer(read_only=True)
    maker_order = serializers.StringRelatedField(read_only=True)
    taker_order = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'trading_pair', 'maker_order', 'taker_order',
            'quantity', 'price', 'maker_fee', 'taker_fee', 'created_at'
        ]


class OrderBookSerializer(serializers.ModelSerializer):
    """Serializer for order book"""
    
    class Meta:
        model = OrderBook
        fields = ['side', 'price', 'quantity', 'order_count']


class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for price history"""
    
    class Meta:
        model = PriceHistory
        fields = [
            'timeframe', 'open_price', 'high_price', 'low_price',
            'close_price', 'volume', 'timestamp'
        ]


class MarketStatsSerializer(serializers.Serializer):
    """Serializer for market statistics"""
    
    symbol = serializers.CharField()
    last_price = serializers.DecimalField(max_digits=20, decimal_places=8)
    price_change = serializers.DecimalField(max_digits=20, decimal_places=8)
    price_change_percent = serializers.DecimalField(max_digits=10, decimal_places=4)
    high_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    low_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    volume_24h = serializers.DecimalField(max_digits=20, decimal_places=8)
    volume_24h_quote = serializers.DecimalField(max_digits=20, decimal_places=8)