from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Wallet, Transaction, DepositAddress, WithdrawalRequest, WalletReservation
from trading.models import Cryptocurrency

class WalletService:
    """Service for wallet operations"""
    
    def get_or_create_wallet(self, user, cryptocurrency):
        """Get or create wallet for user and cryptocurrency"""
        wallet, created = Wallet.objects.get_or_create(
            user=user,
            cryptocurrency=cryptocurrency,
            defaults={
                'available_balance': Decimal('0'),
                'reserved_balance': Decimal('0')
            }
        )
        return wallet
    
    def has_sufficient_balance(self, user, cryptocurrency, amount):
        """Check if user has sufficient balance"""
        wallet = self.get_or_create_wallet(user, cryptocurrency)
        return wallet.available_balance >= amount
    
    def reserve_funds(self, user, cryptocurrency, amount, reason, reference_id=None):
        """Reserve funds in user's wallet"""
        with transaction.atomic():
            wallet = self.get_or_create_wallet(user, cryptocurrency)
            
            if wallet.available_balance < amount:
                raise ValueError("موجودی کافی نیست")
            
            # Move funds from available to reserved
            wallet.available_balance -= amount
            wallet.reserved_balance += amount
            wallet.save()
            
            # Create reservation record
            WalletReservation.objects.create(
                wallet=wallet,
                amount=amount,
                reason=reason,
                reference_id=reference_id
            )
    
    def release_reserved_funds(self, user, cryptocurrency, amount, reason, reference_id=None):
        """Release reserved funds back to available balance"""
        with transaction.atomic():
            wallet = self.get_or_create_wallet(user, cryptocurrency)
            
            if wallet.reserved_balance < amount:
                raise ValueError("موجودی رزرو شده کافی نیست")
            
            # Move funds from reserved to available
            wallet.reserved_balance -= amount
            wallet.available_balance += amount
            wallet.save()
            
            # Mark reservation as released
            if reference_id:
                reservations = WalletReservation.objects.filter(
                    wallet=wallet,
                    reference_id=reference_id,
                    is_active=True
                )
                for reservation in reservations:
                    reservation.is_active = False
                    reservation.released_at = timezone.now()
                    reservation.save()
    
    def transfer_funds(self, user, cryptocurrency, amount, description):
        """Transfer funds (positive for credit, negative for debit)"""
        with transaction.atomic():
            wallet = self.get_or_create_wallet(user, cryptocurrency)
            
            if amount < 0 and wallet.available_balance < abs(amount):
                raise ValueError("موجودی کافی نیست")
            
            # Update wallet balance
            wallet.available_balance += amount
            wallet.save()
            
            # Create transaction record
            Transaction.objects.create(
                wallet=wallet,
                transaction_type='trade' if 'trade' in description.lower() else 'deposit' if amount > 0 else 'withdrawal',
                status='completed',
                amount=amount,
                description=description,
                completed_at=timezone.now()
            )
    
    def create_deposit_transaction(self, user, cryptocurrency, amount, external_tx_id, from_address):
        """Create a deposit transaction"""
        with transaction.atomic():
            wallet = self.get_or_create_wallet(user, cryptocurrency)
            
            # Create transaction
            transaction_obj = Transaction.objects.create(
                wallet=wallet,
                transaction_type='deposit',
                status='pending',
                amount=amount,
                external_tx_id=external_tx_id,
                from_address=from_address,
                description=f"Deposit {amount} {cryptocurrency.symbol}"
            )
            
            return transaction_obj
    
    def confirm_deposit(self, transaction_obj):
        """Confirm a deposit transaction"""
        with transaction.atomic():
            if transaction_obj.status != 'pending':
                raise ValueError("تراکنش قابل تایید نیست")
            
            # Add funds to wallet
            wallet = transaction_obj.wallet
            wallet.available_balance += transaction_obj.amount
            wallet.save()
            
            # Update transaction status
            transaction_obj.status = 'completed'
            transaction_obj.completed_at = timezone.now()
            transaction_obj.save()
    
    def create_withdrawal_request(self, user, cryptocurrency, amount, to_address, tag=None):
        """Create a withdrawal request"""
        with transaction.atomic():
            # Check if user can withdraw
            if not user.is_withdrawal_enabled:
                raise ValueError("برداشت برای حساب شما غیرفعال است")
            
            # Check daily withdrawal limit
            profile = getattr(user, 'profile', None)
            if profile:
                today_withdrawals = WithdrawalRequest.objects.filter(
                    user=user,
                    created_at__date=timezone.now().date(),
                    status__in=['approved', 'processing', 'completed']
                ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
                
                if today_withdrawals + amount > profile.daily_withdrawal_limit:
                    raise ValueError("حد برداشت روزانه تجاوز شده است")
            
            # Calculate fee (simplified - should be based on network conditions)
            fee = amount * Decimal('0.001')  # 0.1% fee
            net_amount = amount - fee
            
            # Check sufficient balance
            if not self.has_sufficient_balance(user, cryptocurrency, amount):
                raise ValueError("موجودی کافی نیست")
            
            # Reserve funds
            self.reserve_funds(user, cryptocurrency, amount, f"Withdrawal to {to_address}")
            
            # Create withdrawal request
            withdrawal_request = WithdrawalRequest.objects.create(
                user=user,
                cryptocurrency=cryptocurrency,
                amount=amount,
                fee=fee,
                net_amount=net_amount,
                to_address=to_address,
                tag=tag
            )
            
            return withdrawal_request
    
    def approve_withdrawal(self, withdrawal_request, approved_by):
        """Approve a withdrawal request"""
        with transaction.atomic():
            if withdrawal_request.status != 'pending':
                raise ValueError("درخواست قابل تایید نیست")
            
            # Update withdrawal request
            withdrawal_request.status = 'approved'
            withdrawal_request.approved_by = approved_by
            withdrawal_request.approved_at = timezone.now()
            withdrawal_request.save()
            
            # Create transaction
            wallet = self.get_or_create_wallet(withdrawal_request.user, withdrawal_request.cryptocurrency)
            transaction_obj = Transaction.objects.create(
                wallet=wallet,
                transaction_type='withdrawal',
                status='processing',
                amount=-withdrawal_request.amount,
                fee=withdrawal_request.fee,
                to_address=withdrawal_request.to_address,
                description=f"Withdrawal {withdrawal_request.amount} {withdrawal_request.cryptocurrency.symbol}"
            )
            
            withdrawal_request.transaction = transaction_obj
            withdrawal_request.save()
            
            return transaction_obj
    
    def complete_withdrawal(self, withdrawal_request, external_tx_id):
        """Complete a withdrawal request"""
        with transaction.atomic():
            if withdrawal_request.status != 'approved':
                raise ValueError("درخواست تایید نشده است")
            
            # Update withdrawal request
            withdrawal_request.status = 'completed'
            withdrawal_request.external_tx_id = external_tx_id
            withdrawal_request.completed_at = timezone.now()
            withdrawal_request.save()
            
            # Update transaction
            if withdrawal_request.transaction:
                withdrawal_request.transaction.status = 'completed'
                withdrawal_request.transaction.external_tx_id = external_tx_id
                withdrawal_request.transaction.completed_at = timezone.now()
                withdrawal_request.transaction.save()
            
            # Remove reserved funds (they were already debited when approved)
            wallet = self.get_or_create_wallet(withdrawal_request.user, withdrawal_request.cryptocurrency)
            wallet.reserved_balance -= withdrawal_request.amount
            wallet.save()
    
    def get_or_create_deposit_address(self, user, cryptocurrency):
        """Get or create deposit address for user"""
        deposit_address, created = DepositAddress.objects.get_or_create(
            user=user,
            cryptocurrency=cryptocurrency,
            defaults={
                'address': self._generate_deposit_address(cryptocurrency),
                'is_active': True
            }
        )
        return deposit_address
    
    def _generate_deposit_address(self, cryptocurrency):
        """Generate a new deposit address (simplified)"""
        # In a real implementation, this would integrate with the blockchain
        # For now, we'll generate a mock address
        import hashlib
        import time
        
        data = f"{cryptocurrency.symbol}{time.time()}"
        hash_obj = hashlib.sha256(data.encode())
        
        if cryptocurrency.symbol == 'BTC':
            return f"bc1q{hash_obj.hexdigest()[:39]}"
        elif cryptocurrency.symbol == 'ETH':
            return f"0x{hash_obj.hexdigest()[:40]}"
        else:
            return f"{cryptocurrency.symbol.lower()}{hash_obj.hexdigest()[:32]}"
    
    def get_wallet_stats(self, user):
        """Get wallet statistics for user"""
        wallets = Wallet.objects.filter(user=user).select_related('cryptocurrency')
        
        total_balance_usd = Decimal('0')
        total_balance_irr = Decimal('0')
        
        # Calculate total balance (simplified - would need real exchange rates)
        for wallet in wallets:
            # Mock exchange rates
            if wallet.cryptocurrency.symbol == 'BTC':
                usd_rate = Decimal('45000')
                irr_rate = Decimal('2650000000')
            elif wallet.cryptocurrency.symbol == 'ETH':
                usd_rate = Decimal('2500')
                irr_rate = Decimal('165000000')
            else:
                usd_rate = Decimal('1')
                irr_rate = Decimal('42000')
            
            balance_usd = wallet.total_balance * usd_rate
            balance_irr = wallet.total_balance * irr_rate
            
            total_balance_usd += balance_usd
            total_balance_irr += balance_irr
        
        # Get transaction stats
        user_transactions = Transaction.objects.filter(wallet__user=user)
        total_deposits = user_transactions.filter(
            transaction_type='deposit', 
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
        
        total_withdrawals = abs(user_transactions.filter(
            transaction_type='withdrawal', 
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0'))
        
        pending_withdrawals = WithdrawalRequest.objects.filter(
            user=user,
            status__in=['pending', 'approved', 'processing']
        ).count()
        
        # Get trading stats
        from trading.models import Trade, Order
        user_orders = Order.objects.filter(user=user)
        total_trades = Trade.objects.filter(
            models.Q(maker_order__in=user_orders) | models.Q(taker_order__in=user_orders)
        ).count()
        
        return {
            'total_balance_usd': total_balance_usd,
            'total_balance_irr': total_balance_irr,
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'pending_withdrawals': pending_withdrawals,
            'total_trades': total_trades,
        }