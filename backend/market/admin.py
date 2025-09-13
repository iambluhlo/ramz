from django.contrib import admin
from .models import MarketData, NewsArticle, MarketAlert, TechnicalIndicator

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = [
        'trading_pair', 'last_price', 'price_change_percent_24h',
        'volume_24h', 'updated_at'
    ]
    list_filter = ['trading_pair__base_currency', 'trading_pair__quote_currency', 'updated_at']
    search_fields = ['trading_pair__symbol']
    readonly_fields = ['updated_at']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'is_published', 'is_featured',
        'published_at', 'created_at'
    ]
    list_filter = ['category', 'is_published', 'is_featured', 'published_at']
    search_fields = ['title', 'content', 'author']
    filter_horizontal = ['related_cryptocurrencies']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('محتوا', {
            'fields': ('title', 'title_en', 'content', 'summary')
        }),
        ('طبقه‌بندی', {
            'fields': ('category', 'tags', 'related_cryptocurrencies')
        }),
        ('اطلاعات نویسنده', {
            'fields': ('author', 'source', 'source_url')
        }),
        ('انتشار', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MarketAlert)
class MarketAlertAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'trading_pair', 'alert_type', 'target_value',
        'status', 'created_at', 'triggered_at'
    ]
    list_filter = ['alert_type', 'status', 'trading_pair', 'created_at']
    search_fields = ['user__email', 'trading_pair__symbol']
    readonly_fields = ['created_at', 'triggered_at']


@admin.register(TechnicalIndicator)
class TechnicalIndicatorAdmin(admin.ModelAdmin):
    list_display = [
        'trading_pair', 'indicator_type', 'timeframe', 'signal',
        'confidence', 'calculated_at'
    ]
    list_filter = ['indicator_type', 'timeframe', 'signal', 'trading_pair']
    search_fields = ['trading_pair__symbol']
    readonly_fields = ['calculated_at']