from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, LoginAttempt, VerificationCode

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'username', 'first_name', 'last_name', 'phone_number',
        'is_phone_verified', 'is_email_verified', 'is_identity_verified',
        'two_factor_enabled', 'is_active', 'date_joined'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_phone_verified',
        'is_email_verified', 'is_identity_verified', 'two_factor_enabled',
        'is_trading_enabled', 'is_withdrawal_enabled'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات شخصی', {
            'fields': ('phone_number', 'national_id')
        }),
        ('وضعیت تایید', {
            'fields': ('is_phone_verified', 'is_email_verified', 'is_identity_verified')
        }),
        ('امنیت', {
            'fields': ('two_factor_enabled', 'two_factor_secret')
        }),
        ('دسترسی‌ها', {
            'fields': ('is_trading_enabled', 'is_withdrawal_enabled')
        }),
        ('اطلاعات سیستم', {
            'fields': ('last_login_ip', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login_ip']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'preferred_language', 'daily_withdrawal_limit', 'created_at']
    list_filter = ['preferred_language', 'city']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'success', 'timestamp']
    list_filter = ['success', 'timestamp']
    search_fields = ['user__email', 'ip_address']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code_type', 'code', 'is_used', 'expires_at', 'created_at']
    list_filter = ['code_type', 'is_used', 'created_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['created_at']
    ordering = ['-created_at']