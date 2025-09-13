from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Notification(models.Model):
    """User notifications"""
    
    NOTIFICATION_TYPES = [
        ('trade_executed', 'معامله اجرا شد'),
        ('order_filled', 'سفارش اجرا شد'),
        ('order_cancelled', 'سفارش لغو شد'),
        ('deposit_confirmed', 'واریز تایید شد'),
        ('withdrawal_approved', 'برداشت تایید شد'),
        ('withdrawal_completed', 'برداشت تکمیل شد'),
        ('price_alert', 'هشدار قیمت'),
        ('security_alert', 'هشدار امنیتی'),
        ('system_maintenance', 'تعمیرات سیستم'),
        ('news_update', 'به‌روزرسانی اخبار'),
        ('account_verified', 'حساب تایید شد'),
        ('kyc_required', 'احراز هویت مورد نیاز'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, verbose_name="نوع اطلاع‌رسانی")
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium', verbose_name="اولویت")
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    message = models.TextField(verbose_name="پیام")
    
    # Optional data for rich notifications
    data = models.JSONField(default=dict, blank=True, verbose_name="داده‌های اضافی")
    
    # Action URL (for clickable notifications)
    action_url = models.URLField(blank=True, null=True, verbose_name="لینک عمل")
    
    # Status
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    is_sent = models.BooleanField(default=False, verbose_name="ارسال شده")
    
    # Delivery channels
    sent_email = models.BooleanField(default=False, verbose_name="ایمیل ارسال شده")
    sent_sms = models.BooleanField(default=False, verbose_name="پیامک ارسال شده")
    sent_push = models.BooleanField(default=False, verbose_name="پوش ارسال شده")
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان خواندن")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان ارسال")
    
    class Meta:
        verbose_name = "اطلاع‌رسانی"
        verbose_name_plural = "اطلاع‌رسانی‌ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_trade_notifications = models.BooleanField(default=True, verbose_name="اطلاع‌رسانی معاملات - ایمیل")
    email_security_alerts = models.BooleanField(default=True, verbose_name="هشدارهای امنیتی - ایمیل")
    email_price_alerts = models.BooleanField(default=True, verbose_name="هشدارهای قیمت - ایمیل")
    email_news_updates = models.BooleanField(default=False, verbose_name="اخبار - ایمیل")
    email_system_updates = models.BooleanField(default=True, verbose_name="به‌روزرسانی‌های سیستم - ایمیل")
    
    # SMS preferences
    sms_trade_notifications = models.BooleanField(default=False, verbose_name="اطلاع‌رسانی معاملات - پیامک")
    sms_security_alerts = models.BooleanField(default=True, verbose_name="هشدارهای امنیتی - پیامک")
    sms_price_alerts = models.BooleanField(default=False, verbose_name="هشدارهای قیمت - پیامک")
    sms_withdrawal_confirmations = models.BooleanField(default=True, verbose_name="تایید برداشت - پیامک")
    
    # Push notification preferences
    push_trade_notifications = models.BooleanField(default=True, verbose_name="اطلاع‌رسانی معاملات - پوش")
    push_security_alerts = models.BooleanField(default=True, verbose_name="هشدارهای امنیتی - پوش")
    push_price_alerts = models.BooleanField(default=True, verbose_name="هشدارهای قیمت - پوش")
    push_news_updates = models.BooleanField(default=True, verbose_name="اخبار - پوش")
    push_system_updates = models.BooleanField(default=True, verbose_name="به‌روزرسانی‌های سیستم - پوش")
    
    # General preferences
    do_not_disturb_start = models.TimeField(null=True, blank=True, verbose_name="شروع حالت مزاحم نشوید")
    do_not_disturb_end = models.TimeField(null=True, blank=True, verbose_name="پایان حالت مزاحم نشوید")
    timezone = models.CharField(max_length=50, default='Asia/Tehran', verbose_name="منطقه زمانی")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تنظیمات اطلاع‌رسانی"
        verbose_name_plural = "تنظیمات اطلاع‌رسانی"
    
    def __str__(self):
        return f"تنظیمات {self.user.email}"


class EmailTemplate(models.Model):
    """Email templates for notifications"""
    
    TEMPLATE_TYPES = [
        ('trade_executed', 'معامله اجرا شد'),
        ('order_filled', 'سفارش اجرا شد'),
        ('deposit_confirmed', 'واریز تایید شد'),
        ('withdrawal_approved', 'برداشت تایید شد'),
        ('price_alert', 'هشدار قیمت'),
        ('security_alert', 'هشدار امنیتی'),
        ('welcome', 'خوش‌آمدگویی'),
        ('verification', 'تایید حساب'),
        ('password_reset', 'بازیابی رمز عبور'),
    ]
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, unique=True, verbose_name="نوع قالب")
    
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    html_content = models.TextField(verbose_name="محتوای HTML")
    text_content = models.TextField(verbose_name="محتوای متنی")
    
    # Template variables documentation
    variables = models.JSONField(
        default=list, 
        blank=True,
        help_text="متغیرهای قابل استفاده در قالب",
        verbose_name="متغیرها"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "قالب ایمیل"
        verbose_name_plural = "قالب‌های ایمیل"
    
    def __str__(self):
        return f"{self.get_template_type_display()} - {self.subject}"


class SMSTemplate(models.Model):
    """SMS templates for notifications"""
    
    TEMPLATE_TYPES = [
        ('verification_code', 'کد تایید'),
        ('trade_executed', 'معامله اجرا شد'),
        ('security_alert', 'هشدار امنیتی'),
        ('withdrawal_confirmation', 'تایید برداشت'),
        ('price_alert', 'هشدار قیمت'),
    ]
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, unique=True, verbose_name="نوع قالب")
    content = models.TextField(max_length=160, verbose_name="محتوا")  # SMS character limit
    
    # Template variables
    variables = models.JSONField(
        default=list, 
        blank=True,
        verbose_name="متغیرها"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "قالب پیامک"
        verbose_name_plural = "قالب‌های پیامک"
    
    def __str__(self):
        return f"{self.get_template_type_display()}"


class NotificationLog(models.Model):
    """Log of sent notifications for tracking and debugging"""
    
    DELIVERY_STATUS = [
        ('pending', 'در انتظار'),
        ('sent', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('failed', 'ناموفق'),
        ('bounced', 'برگشت خورده'),
    ]
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name="اطلاع‌رسانی")
    
    delivery_method = models.CharField(
        max_length=10,
        choices=[
            ('email', 'ایمیل'),
            ('sms', 'پیامک'),
            ('push', 'پوش'),
        ],
        verbose_name="روش ارسال"
    )
    
    recipient = models.CharField(max_length=200, verbose_name="گیرنده")  # email or phone number
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='pending', verbose_name="وضعیت")
    
    # Provider response
    provider_response = models.JSONField(default=dict, blank=True, verbose_name="پاسخ ارائه‌دهنده")
    error_message = models.TextField(blank=True, null=True, verbose_name="پیام خطا")
    
    # Tracking
    external_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شناسه خارجی")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "لاگ اطلاع‌رسانی"
        verbose_name_plural = "لاگ‌های اطلاع‌رسانی"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification.title} - {self.delivery_method} - {self.status}"