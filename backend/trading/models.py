from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid

User = get_user_model()

class Cryptocurrency(models.Model):
    """Cryptocurrency model"""
    
    symbol = models.CharField(max_length=10, unique=True, verbose_name="نماد")
    name = models.CharField(max_length=100, verbose_name="نام")
    name_fa = models.CharField(max_length=100, verbose_name="نام فارسی")
    
    # Trading settings
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    min_trade_amount = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0.00000001'),
        verbose_name="حداقل مقدار معامله"
    )
    max_trade_amount = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="حداکثر مقدار معامله"
    )
    
    # Fees
    maker_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.001'),
        verbose_name="کارمزد سازنده"
    )
    taker_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.001'),
        verbose_name="کارمزد گیرنده"
    )
    
    # Network settings
    network = models.CharField(max_length=50, default='mainnet', verbose_name="شبکه")
    contract_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="آدرس قرارداد")
    decimals = models.IntegerField(default=8, verbose_name="تعداد اعشار")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ارز دیجیتال"
        verbose_name_plural = "ارزهای دیجیتال"
        ordering = ['symbol']
    
    def __str__(self):
        return f"{self.symbol} - {self.name_fa}"


class TradingPair(models.Model):
    """Trading pair model"""
    
    base_currency = models.ForeignKey(
        Cryptocurrency, 
        on_delete=models.CASCADE, 
        related_name='base_pairs',
        verbose_name="ارز پایه"
    )
    quote_currency = models.ForeignKey(
        Cryptocurrency, 
        on_delete=models.CASCADE, 
        related_name='quote_pairs',
        verbose_name="ارز نقل قول"
    )
    
    symbol = models.CharField(max_length=20, unique=True, verbose_name="نماد جفت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    # Price settings
    min_price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0.00000001'),
        verbose_name="حداقل قیمت"
    )
    max_price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="حداکثر قیمت"
    )
    price_precision = models.IntegerField(default=8, verbose_name="دقت قیمت")
    quantity_precision = models.IntegerField(default=8, verbose_name="دقت مقدار")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "جفت معاملاتی"
        verbose_name_plural = "جفت‌های معاملاتی"
        unique_together = ['base_currency', 'quote_currency']
    
    def __str__(self):
        return self.symbol
    
    def save(self, *args, **kwargs):
        if not self.symbol:
            self.symbol = f"{self.base_currency.symbol}/{self.quote_currency.symbol}"
        super().save(*args, **kwargs)


class Order(models.Model):
    """Order model"""
    
    ORDER_TYPES = [
        ('market', 'بازار'),
        ('limit', 'محدود'),
        ('stop', 'استاپ'),
        ('stop_limit', 'استاپ محدود'),
    ]
    
    ORDER_SIDES = [
        ('buy', 'خرید'),
        ('sell', 'فروش'),
    ]
    
    ORDER_STATUS = [
        ('pending', 'در انتظار'),
        ('partially_filled', 'تا حدی اجرا شده'),
        ('filled', 'اجرا شده'),
        ('cancelled', 'لغو شده'),
        ('rejected', 'رد شده'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, verbose_name="جفت معاملاتی")
    
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, verbose_name="نوع سفارش")
    side = models.CharField(max_length=10, choices=ORDER_SIDES, verbose_name="نوع معامله")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name="وضعیت")
    
    # Quantities and prices
    quantity = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="قیمت"
    )
    stop_price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="قیمت استاپ"
    )
    
    filled_quantity = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0'),
        verbose_name="مقدار اجرا شده"
    )
    remaining_quantity = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0'),
        verbose_name="مقدار باقی‌مانده"
    )
    
    # Fees
    fee = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0'),
        verbose_name="کارمزد"
    )
    fee_currency = models.ForeignKey(
        Cryptocurrency, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="ارز کارمزد"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    executed_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان اجرا")
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.side} {self.quantity} {self.trading_pair.symbol}"
    
    def save(self, *args, **kwargs):
        if not self.remaining_quantity:
            self.remaining_quantity = self.quantity - self.filled_quantity
        super().save(*args, **kwargs)


class Trade(models.Model):
    """Trade execution model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, verbose_name="جفت معاملاتی")
    
    # Orders involved
    maker_order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='maker_trades',
        verbose_name="سفارش سازنده"
    )
    taker_order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='taker_trades',
        verbose_name="سفارش گیرنده"
    )
    
    # Trade details
    quantity = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت")
    
    # Fees
    maker_fee = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="کارمزد سازنده")
    taker_fee = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="کارمزد گیرنده")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.quantity} @ {self.price}"


class OrderBook(models.Model):
    """Order book model for real-time data"""
    
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, verbose_name="جفت معاملاتی")
    side = models.CharField(max_length=10, choices=Order.ORDER_SIDES, verbose_name="نوع")
    price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت")
    quantity = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    order_count = models.IntegerField(default=1, verbose_name="تعداد سفارشات")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "دفتر سفارشات"
        verbose_name_plural = "دفتر سفارشات"
        unique_together = ['trading_pair', 'side', 'price']
        ordering = ['trading_pair', 'side', '-price']
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.side} {self.quantity} @ {self.price}"


class PriceHistory(models.Model):
    """Price history for charts"""
    
    TIMEFRAMES = [
        ('1m', '1 دقیقه'),
        ('5m', '5 دقیقه'),
        ('15m', '15 دقیقه'),
        ('1h', '1 ساعت'),
        ('4h', '4 ساعت'),
        ('1d', '1 روز'),
        ('1w', '1 هفته'),
    ]
    
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, verbose_name="جفت معاملاتی")
    timeframe = models.CharField(max_length=5, choices=TIMEFRAMES, verbose_name="بازه زمانی")
    
    # OHLCV data
    open_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت باز")
    high_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="بالاترین قیمت")
    low_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="پایین‌ترین قیمت")
    close_price = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="قیمت بسته")
    volume = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="حجم")
    
    timestamp = models.DateTimeField(verbose_name="زمان")
    
    class Meta:
        verbose_name = "تاریخچه قیمت"
        verbose_name_plural = "تاریخچه قیمت‌ها"
        unique_together = ['trading_pair', 'timeframe', 'timestamp']
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.trading_pair.symbol} - {self.timeframe} - {self.timestamp}"