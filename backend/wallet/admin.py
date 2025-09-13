from django.contrib import admin
from .models import Wallet, Transaction, DepositAddress, WithdrawalRequest, WalletReservation

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'cryptocurrency', 'available_balance', 'reserved_balance',
        'total_balance', 'created_at'
    ]
    list_filter = ['cryptocurrency', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def total_balance(self, obj):
        return obj.total_balance
    total_balance.short_description = 'کل موجودی'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'wallet', 'transaction_type', 'status', 'amount', 'fee',
        'confirmations', 'created_at'
    ]
    list_filter = ['transaction_type', 'status', 'wallet__cryptocurrency', 'created_at']
    search_fields = ['id', 'wallet__user__email', 'external_tx_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'wallet__user', 'wallet__cryptocurrency'
        )


@admin.register(DepositAddress)
class DepositAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'cryptocurrency', 'address', 'tag', 'is_active', 'created_at']
    list_filter = ['cryptocurrency', 'is_active', 'created_at']
    search_fields = ['user__email', 'address']
    readonly_fields = ['created_at', 'last_used_at']


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'cryptocurrency', 'amount', 'fee', 'status',
        'to_address', 'created_at'
    ]
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['id', 'user__email', 'to_address', 'external_tx_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    actions = ['approve_withdrawals', 'reject_withdrawals']
    
    def approve_withdrawals(self, request, queryset):
        from .services import WalletService
        wallet_service = WalletService()
        
        approved_count = 0
        for withdrawal in queryset.filter(status='pending'):
            try:
                wallet_service.approve_withdrawal(withdrawal, request.user)
                approved_count += 1
            except Exception as e:
                self.message_user(request, f"خطا در تایید {withdrawal.id}: {str(e)}")
        
        self.message_user(request, f"{approved_count} درخواست تایید شد")
    
    approve_withdrawals.short_description = "تایید درخواست‌های انتخاب شده"
    
    def reject_withdrawals(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} درخواست رد شد")
    
    reject_withdrawals.short_description = "رد درخواست‌های انتخاب شده"


@admin.register(WalletReservation)
class WalletReservationAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'reason', 'reference_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['wallet__user__email', 'reason', 'reference_id']
    readonly_fields = ['created_at', 'released_at']