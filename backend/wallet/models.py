from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid

User = get_user_model()

class Wallet(models.Model):
    """User wallet for each cryptocurrency"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    cryptocurrency = models.ForeignKey(
        'trading.Cryptocurrency', 
        on_delete=models.CASCADE,
        verbose_name="ارز دیجیتال"
    )
    
    # Balances
    available_balance = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0'),
        verbose_name="موجودی قابل استفاده"
    )
    reserved_balance = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        default=Decimal('0'),
        verbose_name="موجودی رزرو شده"
    )
    
    # Wallet address for deposits
    deposit_address = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="آدرس واریز"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف‌های پول"
        unique_together = ['user', 'cryptocurrency']
    
    def __str__(self):
        return f"{self.user.email} - {self.cryptocurrency.symbol}"
    
    @property
    def total_balance(self):
        return self.available_balance + self.reserved_balance


class Transaction(models.Model):
    """Wallet transaction model"""
    
    TRANSACTION_TYPES = [
        ('deposit', 'واریز'),
        ('withdrawal', 'برداشت'),
        ('trade', 'معامله'),
        ('fee', 'کارمزد'),
        ('bonus', 'پاداش'),
        ('penalty', 'جریمه'),
    ]
    
    TRANSACTION_STATUS = [
        ('pending', 'در انتظار'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="کیف پول")
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="نوع تراکنش")
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending', verbose_name="وضعیت")
    
    amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'), verbose_name="کارمزد")
    
    # External transaction details
    external_tx_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه تراکنش خارجی")
    from_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="آدرس مبدا")
    to_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="آدرس مقصد")
    
    # Network confirmations
    confirmations = models.IntegerField(default=0, verbose_name="تعداد تاییدیه")
    required_confirmations = models.IntegerField(default=6, verbose_name="تاییدیه‌های مورد نیاز")
    
    # Additional info
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="اطلاعات اضافی")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان تکمیل")
    
    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.wallet.user.email} - {self.get_transaction_type_display()} - {self.amount}"


class DepositAddress(models.Model):
    """Deposit addresses for users"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    cryptocurrency = models.ForeignKey(
        'trading.Cryptocurrency', 
        on_delete=models.CASCADE,
        verbose_name="ارز دیجیتال"
    )
    
    address = models.CharField(max_length=100, unique=True, verbose_name="آدرس")
    tag = models.CharField(max_length=50, blank=True, null=True, verbose_name="تگ/Memo")
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name="آخرین استفاده")
    
    class Meta:
        verbose_name = "آدرس واریز"
        verbose_name_plural = "آدرس‌های واریز"
        unique_together = ['user', 'cryptocurrency']
    
    def __str__(self):
        return f"{self.user.email} - {self.cryptocurrency.symbol} - {self.address}"


class WithdrawalRequest(models.Model):
    """Withdrawal request model"""
    
    WITHDRAWAL_STATUS = [
        ('pending', 'در انتظار'),
        ('approved', 'تایید شده'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('rejected', 'رد شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    cryptocurrency = models.ForeignKey(
        'trading.Cryptocurrency', 
        on_delete=models.CASCADE,
        verbose_name="ارز دیجیتال"
    )
    
    amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    fee = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="کارمزد")
    net_amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار خالص")
    
    to_address = models.CharField(max_length=100, verbose_name="آدرس مقصد")
    tag = models.CharField(max_length=50, blank=True, null=True, verbose_name="تگ/Memo")
    
    status = models.CharField(max_length=20, choices=WITHDRAWAL_STATUS, default='pending', verbose_name="وضعیت")
    
    # Admin fields
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_withdrawals',
        verbose_name="تایید شده توسط"
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان تایید")
    
    # Transaction details
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="تراکنش"
    )
    external_tx_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه تراکنش")
    
    # Additional info
    notes = models.TextField(blank=True, null=True, verbose_name="یادداشت‌ها")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان تکمیل")
    
    class Meta:
        verbose_name = "درخواست برداشت"
        verbose_name_plural = "درخواست‌های برداشت"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.cryptocurrency.symbol}"


class WalletReservation(models.Model):
    """Track reserved funds for orders"""
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="کیف پول")
    amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="مقدار")
    reason = models.CharField(max_length=200, verbose_name="دلیل")
    
    # Reference to the order or transaction that caused this reservation
    reference_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه مرجع")
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان آزادسازی")
    
    class Meta:
        verbose_name = "رزرو کیف پول"
        verbose_name_plural = "رزروهای کیف پول"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.wallet} - {self.amount} - {self.reason}"