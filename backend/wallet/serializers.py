from rest_framework import serializers
from decimal import Decimal
from .models import Wallet, Transaction, DepositAddress, WithdrawalRequest
from trading.serializers import CryptocurrencySerializer

class WalletSerializer(serializers.ModelSerializer):
    """Serializer for wallet"""
    
    cryptocurrency = CryptocurrencySerializer(read_only=True)
    total_balance = serializers.ReadOnlyField()
    
    class Meta:
        model = Wallet
        fields = [
            'id', 'cryptocurrency', 'available_balance', 'reserved_balance',
            'total_balance', 'deposit_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'available_balance', 'reserved_balance', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transactions"""
    
    wallet = WalletSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'wallet', 'transaction_type', 'status', 'amount', 'fee',
            'external_tx_id', 'from_address', 'to_address', 'confirmations',
            'required_confirmations', 'description', 'created_at', 'updated_at',
            'completed_at'
        ]
        read_only_fields = [
            'id', 'status', 'confirmations', 'created_at', 'updated_at', 'completed_at'
        ]


class DepositAddressSerializer(serializers.ModelSerializer):
    """Serializer for deposit addresses"""
    
    cryptocurrency = CryptocurrencySerializer(read_only=True)
    
    class Meta:
        model = DepositAddress
        fields = [
            'cryptocurrency', 'address', 'tag', 'is_active', 'created_at', 'last_used_at'
        ]
        read_only_fields = ['created_at', 'last_used_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    """Serializer for withdrawal requests"""
    
    cryptocurrency = CryptocurrencySerializer(read_only=True)
    cryptocurrency_id = serializers.IntegerField(write_only=True)
    net_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = WithdrawalRequest
        fields = [
            'id', 'cryptocurrency', 'cryptocurrency_id', 'amount', 'fee',
            'net_amount', 'to_address', 'tag', 'status', 'external_tx_id',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'fee', 'net_amount', 'status', 'external_tx_id',
            'created_at', 'updated_at', 'completed_at'
        ]
    
    def validate(self, attrs):
        cryptocurrency_id = attrs.get('cryptocurrency_id')
        amount = attrs.get('amount')
        to_address = attrs.get('to_address')
        
        # Validate cryptocurrency
        try:
            from trading.models import Cryptocurrency
            cryptocurrency = Cryptocurrency.objects.get(id=cryptocurrency_id, is_active=True)
            attrs['cryptocurrency'] = cryptocurrency
        except Cryptocurrency.DoesNotExist:
            raise serializers.ValidationError("ارز دیجیتال نامعتبر است")
        
        # Validate amount
        if amount <= 0:
            raise serializers.ValidationError("مقدار باید مثبت باشد")
        
        if amount < cryptocurrency.min_trade_amount:
            raise serializers.ValidationError(
                f"مقدار نمی‌تواند کمتر از {cryptocurrency.min_trade_amount} باشد"
            )
        
        # Validate address format (basic validation)
        if not to_address or len(to_address) < 10:
            raise serializers.ValidationError("آدرس نامعتبر است")
        
        return attrs


class CreateWithdrawalSerializer(serializers.Serializer):
    """Serializer for creating withdrawal requests"""
    
    cryptocurrency_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    to_address = serializers.CharField(max_length=100)
    tag = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate(self, attrs):
        cryptocurrency_id = attrs.get('cryptocurrency_id')
        amount = attrs.get('amount')
        to_address = attrs.get('to_address')
        
        # Validate cryptocurrency
        try:
            from trading.models import Cryptocurrency
            cryptocurrency = Cryptocurrency.objects.get(id=cryptocurrency_id, is_active=True)
            attrs['cryptocurrency'] = cryptocurrency
        except Cryptocurrency.DoesNotExist:
            raise serializers.ValidationError("ارز دیجیتال نامعتبر است")
        
        # Validate amount
        if amount <= 0:
            raise serializers.ValidationError("مقدار باید مثبت باشد")
        
        # Check minimum withdrawal amount
        min_withdrawal = getattr(cryptocurrency, 'min_withdrawal_amount', cryptocurrency.min_trade_amount)
        if amount < min_withdrawal:
            raise serializers.ValidationError(
                f"حداقل مقدار برداشت {min_withdrawal} {cryptocurrency.symbol} است"
            )
        
        # Validate address
        if not to_address or len(to_address) < 10:
            raise serializers.ValidationError("آدرس نامعتبر است")
        
        return attrs


class WalletStatsSerializer(serializers.Serializer):
    """Serializer for wallet statistics"""
    
    total_balance_usd = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_balance_irr = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_deposits = serializers.DecimalField(max_digits=20, decimal_places=8)
    total_withdrawals = serializers.DecimalField(max_digits=20, decimal_places=8)
    pending_withdrawals = serializers.IntegerField()
    total_trades = serializers.IntegerField()