from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid

class User(AbstractUser):
    """Custom User model with additional fields for crypto trading platform"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="شماره تلفن باید به فرمت 09xxxxxxxxx باشد"
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=11, 
        unique=True,
        verbose_name="شماره تلفن"
    )
    
    # Personal Information
    first_name = models.CharField(max_length=30, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    national_id = models.CharField(
        max_length=10, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="کد ملی"
    )
    
    # Verification Status
    is_phone_verified = models.BooleanField(default=False, verbose_name="تلفن تایید شده")
    is_email_verified = models.BooleanField(default=False, verbose_name="ایمیل تایید شده")
    is_identity_verified = models.BooleanField(default=False, verbose_name="هویت تایید شده")
    
    # Security
    two_factor_enabled = models.BooleanField(default=False, verbose_name="احراز هویت دو مرحله‌ای")
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    
    # Account Status
    is_trading_enabled = models.BooleanField(default=True, verbose_name="معاملات فعال")
    is_withdrawal_enabled = models.BooleanField(default=True, verbose_name="برداشت فعال")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    """Extended user profile information"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Address Information
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="شهر")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد پستی")
    
    # Documents
    identity_document = models.ImageField(
        upload_to='documents/identity/', 
        blank=True, 
        null=True,
        verbose_name="تصویر کارت ملی"
    )
    selfie_document = models.ImageField(
        upload_to='documents/selfie/', 
        blank=True, 
        null=True,
        verbose_name="تصویر سلفی"
    )
    
    # Trading Preferences
    preferred_language = models.CharField(
        max_length=5, 
        choices=[('fa', 'فارسی'), ('en', 'English')], 
        default='fa'
    )
    
    # Risk Management
    daily_withdrawal_limit = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=500000000,  # 500M Toman
        verbose_name="حد برداشت روزانه"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"
    
    def __str__(self):
        return f"پروفایل {self.user.full_name}"


class LoginAttempt(models.Model):
    """Track login attempts for security"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "تلاش ورود"
        verbose_name_plural = "تلاش‌های ورود"
        ordering = ['-timestamp']


class VerificationCode(models.Model):
    """Store verification codes for phone/email verification"""
    
    CODE_TYPES = [
        ('phone', 'تلفن'),
        ('email', 'ایمیل'),
        ('2fa_setup', 'تنظیم احراز دو مرحله‌ای'),
        ('password_reset', 'بازیابی رمز عبور'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    code_type = models.CharField(max_length=20, choices=CODE_TYPES)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کدهای تایید"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_code_type_display()}"