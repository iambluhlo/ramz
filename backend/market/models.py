from django.db import models
from decimal import Decimal

class MarketData(models.Model):
    """Real-time market data"""
    
    trading_pair = models.ForeignKey(
        'trading.TradingPair', 
        on_delete=models.CASCADE,
        verbose_name="جفت معاملاتی"
    )
    
    # Current prices
    last_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="آخرین قیمت")
    bid_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت خرید")
    ask_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت فروش")
    
    # 24h statistics
    high_24h = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="بالاترین قیمت 24 ساعته")
    low_24h = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="پایین‌ترین قیمت 24 ساعته")
    volume_24h = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="حجم 24 ساعته")
    volume_24h_quote = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="حجم 24 ساعته (نقل قول)")
    
    # Price changes
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="تغییر قیمت 24 ساعته")
    price_change_percent_24h = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="درصد تغییر قیمت 24 ساعته")
    
    # Market cap and supply (for informational purposes)
    market_cap = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="ارزش بازار"
    )
    circulating_supply = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="عرضه در گردش"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "داده بازار"
        verbose_name_plural = "داده‌های بازار"
        unique_together = ['trading_pair']
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.last_price}"


class NewsArticle(models.Model):
    """Crypto news articles"""
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="عنوان انگلیسی")
    
    content = models.TextField(verbose_name="محتوا")
    summary = models.TextField(max_length=500, verbose_name="خلاصه")
    
    # Related cryptocurrencies
    related_cryptocurrencies = models.ManyToManyField(
        'trading.Cryptocurrency',
        blank=True,
        verbose_name="ارزهای مرتبط"
    )
    
    # Article metadata
    author = models.CharField(max_length=100, verbose_name="نویسنده")
    source = models.CharField(max_length=100, verbose_name="منبع")
    source_url = models.URLField(blank=True, null=True, verbose_name="لینک منبع")
    
    # SEO and categorization
    category = models.CharField(
        max_length=50,
        choices=[
            ('market', 'بازار'),
            ('technology', 'فناوری'),
            ('regulation', 'قانون‌گذاری'),
            ('adoption', 'پذیرش'),
            ('analysis', 'تحلیل'),
            ('news', 'اخبار عمومی'),
        ],
        default='news',
        verbose_name="دسته‌بندی"
    )
    
    tags = models.CharField(max_length=200, blank=True, verbose_name="برچسب‌ها")
    
    # Publication info
    is_published = models.BooleanField(default=False, verbose_name="منتشر شده")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان انتشار")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "مقاله خبری"
        verbose_name_plural = "مقالات خبری"
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title


class MarketAlert(models.Model):
    """Price alerts for users"""
    
    ALERT_TYPES = [
        ('price_above', 'قیمت بالاتر از'),
        ('price_below', 'قیمت پایین‌تر از'),
        ('price_change', 'تغییر قیمت'),
        ('volume_spike', 'افزایش حجم'),
    ]
    
    ALERT_STATUS = [
        ('active', 'فعال'),
        ('triggered', 'اجرا شده'),
        ('expired', 'منقضی شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    trading_pair = models.ForeignKey(
        'trading.TradingPair', 
        on_delete=models.CASCADE,
        verbose_name="جفت معاملاتی"
    )
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, verbose_name="نوع هشدار")
    target_value = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار هدف")
    
    status = models.CharField(max_length=20, choices=ALERT_STATUS, default='active', verbose_name="وضعیت")
    
    # Notification settings
    notify_email = models.BooleanField(default=True, verbose_name="اطلاع‌رسانی ایمیل")
    notify_sms = models.BooleanField(default=False, verbose_name="اطلاع‌رسانی پیامک")
    notify_push = models.BooleanField(default=True, verbose_name="اطلاع‌رسانی پوش")
    
    # Expiration
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان انقضا")
    
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان اجرا")
    
    class Meta:
        verbose_name = "هشدار بازار"
        verbose_name_plural = "هشدارهای بازار"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.trading_pair.symbol} - {self.get_alert_type_display()}"


class TechnicalIndicator(models.Model):
    """Technical analysis indicators"""
    
    INDICATOR_TYPES = [
        ('sma', 'میانگین متحرک ساده'),
        ('ema', 'میانگین متحرک نمایی'),
        ('rsi', 'شاخص قدرت نسبی'),
        ('macd', 'MACD'),
        ('bollinger', 'باند بولینگر'),
        ('stochastic', 'استوکاستیک'),
    ]
    
    TIMEFRAMES = [
        ('1m', '1 دقیقه'),
        ('5m', '5 دقیقه'),
        ('15m', '15 دقیقه'),
        ('1h', '1 ساعت'),
        ('4h', '4 ساعت'),
        ('1d', '1 روز'),
    ]
    
    trading_pair = models.ForeignKey(
        'trading.TradingPair', 
        on_delete=models.CASCADE,
        verbose_name="جفت معاملاتی"
    )
    
    indicator_type = models.CharField(max_length=20, choices=INDICATOR_TYPES, verbose_name="نوع شاخص")
    timeframe = models.CharField(max_length=5, choices=TIMEFRAMES, verbose_name="بازه زمانی")
    
    # Indicator values (stored as JSON for flexibility)
    values = models.JSONField(verbose_name="مقادیر")
    
    # Signal interpretation
    signal = models.CharField(
        max_length=10,
        choices=[
            ('buy', 'خرید'),
            ('sell', 'فروش'),
            ('hold', 'نگهداری'),
            ('neutral', 'خنثی'),
        ],
        default='neutral',
        verbose_name="سیگنال"
    )
    
    confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0'),
        verbose_name="اعتماد"
    )
    
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "شاخص تکنیکال"
        verbose_name_plural = "شاخص‌های تکنیکال"
        unique_together = ['trading_pair', 'indicator_type', 'timeframe']
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.get_indicator_type_display()} - {self.timeframe}"