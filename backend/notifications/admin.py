from django.contrib import admin
from .models import Notification, NotificationPreference, EmailTemplate, SMSTemplate, NotificationLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'notification_type', 'priority', 'title', 'is_read',
        'is_sent', 'created_at'
    ]
    list_filter = [
        'notification_type', 'priority', 'is_read', 'is_sent', 'created_at'
    ]
    search_fields = ['user__email', 'title', 'message']
    readonly_fields = ['id', 'created_at', 'read_at', 'sent_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'notification_type', 'priority', 'title', 'message')
        }),
        ('داده‌های اضافی', {
            'fields': ('data', 'action_url'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_read', 'is_sent', 'sent_email', 'sent_sms', 'sent_push')
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'read_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_trade_notifications', 'sms_security_alerts', 'push_price_alerts']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('تنظیمات ایمیل', {
            'fields': (
                'email_trade_notifications', 'email_security_alerts', 
                'email_price_alerts', 'email_news_updates', 'email_system_updates'
            )
        }),
        ('تنظیمات پیامک', {
            'fields': (
                'sms_trade_notifications', 'sms_security_alerts', 
                'sms_price_alerts', 'sms_withdrawal_confirmations'
            )
        }),
        ('تنظیمات پوش', {
            'fields': (
                'push_trade_notifications', 'push_security_alerts', 
                'push_price_alerts', 'push_news_updates', 'push_system_updates'
            )
        }),
        ('تنظیمات عمومی', {
            'fields': ('do_not_disturb_start', 'do_not_disturb_end', 'timezone')
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_type', 'subject', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['subject', 'html_content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_type', 'content', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'notification', 'delivery_method', 'recipient', 'status', 'created_at'
    ]
    list_filter = ['delivery_method', 'status', 'created_at']
    search_fields = ['recipient', 'notification__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('notification__user')