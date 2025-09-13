from django.contrib import admin
from .models import Cryptocurrency, TradingPair, Order, Trade, OrderBook, PriceHistory

@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'symbol', 'name', 'name_fa', 'is_active', 'min_trade_amount',
        'maker_fee', 'taker_fee', 'network'
    ]
    list_filter = ['is_active', 'network']
    search_fields = ['symbol', 'name', 'name_fa']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TradingPair)
class TradingPairAdmin(admin.ModelAdmin):
    list_display = [
        'symbol', 'base_currency', 'quote_currency', 'is_active',
        'price_precision', 'quantity_precision'
    ]
    list_filter = ['is_active', 'base_currency', 'quote_currency']
    search_fields = ['symbol']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'trading_pair', 'order_type', 'side', 'status',
        'quantity', 'price', 'filled_quantity', 'created_at'
    ]
    list_filter = ['order_type', 'side', 'status', 'trading_pair', 'created_at']
    search_fields = ['user__email', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'executed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'trading_pair__base_currency', 'trading_pair__quote_currency'
        )


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trading_pair', 'quantity', 'price', 'maker_fee', 'taker_fee', 'created_at'
    ]
    list_filter = ['trading_pair', 'created_at']
    search_fields = ['id', 'maker_order__user__email', 'taker_order__user__email']
    readonly_fields = ['id', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'trading_pair', 'maker_order__user', 'taker_order__user'
        )


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['trading_pair', 'side', 'price', 'quantity', 'order_count', 'updated_at']
    list_filter = ['trading_pair', 'side']
    readonly_fields = ['updated_at']


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'trading_pair', 'timeframe', 'open_price', 'high_price', 
        'low_price', 'close_price', 'volume', 'timestamp'
    ]
    list_filter = ['trading_pair', 'timeframe', 'timestamp']
    readonly_fields = ['timestamp']