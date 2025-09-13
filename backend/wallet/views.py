from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Wallet, Transaction, DepositAddress, WithdrawalRequest
from .serializers import (
    WalletSerializer, TransactionSerializer, DepositAddressSerializer,
    WithdrawalRequestSerializer, CreateWithdrawalSerializer, WalletStatsSerializer
)
from .services import WalletService
from trading.models import Cryptocurrency

class UserWalletsView(generics.ListAPIView):
    """List user's wallets"""
    
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get or create wallets for all active cryptocurrencies
        wallet_service = WalletService()
        cryptocurrencies = Cryptocurrency.objects.filter(is_active=True)
        
        for crypto in cryptocurrencies:
            wallet_service.get_or_create_wallet(self.request.user, crypto)
        
        return Wallet.objects.filter(user=self.request.user).select_related('cryptocurrency')


class UserTransactionsView(generics.ListAPIView):
    """List user's transactions"""
    
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(
            wallet__user=self.request.user
        ).select_related('wallet__cryptocurrency')
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by cryptocurrency
        crypto_filter = self.request.query_params.get('cryptocurrency')
        if crypto_filter:
            queryset = queryset.filter(wallet__cryptocurrency_id=crypto_filter)
        
        return queryset.order_by('-created_at')


class DepositAddressView(generics.RetrieveAPIView):
    """Get deposit address for a cryptocurrency"""
    
    serializer_class = DepositAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        crypto_id = self.kwargs.get('crypto_id')
        try:
            cryptocurrency = Cryptocurrency.objects.get(id=crypto_id, is_active=True)
        except Cryptocurrency.DoesNotExist:
            raise Http404("ارز دیجیتال یافت نشد")
        
        wallet_service = WalletService()
        return wallet_service.get_or_create_deposit_address(self.request.user, cryptocurrency)


class CreateWithdrawalView(generics.CreateAPIView):
    """Create withdrawal request"""
    
    serializer_class = CreateWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user can withdraw
        if not request.user.is_withdrawal_enabled:
            return Response(
                {'error': 'برداشت برای حساب شما غیرفعال است'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create withdrawal request using service
        wallet_service = WalletService()
        try:
            withdrawal_request = wallet_service.create_withdrawal_request(
                user=request.user,
                **serializer.validated_data
            )
            
            return Response(
                WithdrawalRequestSerializer(withdrawal_request).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserWithdrawalsView(generics.ListAPIView):
    """List user's withdrawal requests"""
    
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = WithdrawalRequest.objects.filter(
            user=self.request.user
        ).select_related('cryptocurrency')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by cryptocurrency
        crypto_filter = self.request.query_params.get('cryptocurrency')
        if crypto_filter:
            queryset = queryset.filter(cryptocurrency_id=crypto_filter)
        
        return queryset.order_by('-created_at')


class CancelWithdrawalView(generics.UpdateAPIView):
    """Cancel withdrawal request"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, withdrawal_id):
        try:
            withdrawal_request = WithdrawalRequest.objects.get(
                id=withdrawal_id, 
                user=request.user
            )
        except WithdrawalRequest.DoesNotExist:
            return Response(
                {'error': 'درخواست برداشت یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if withdrawal_request.status != 'pending':
            return Response(
                {'error': 'این درخواست قابل لغو نیست'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel withdrawal and release reserved funds
        wallet_service = WalletService()
        try:
            wallet_service.release_reserved_funds(
                request.user,
                withdrawal_request.cryptocurrency,
                withdrawal_request.amount,
                f"Cancelled withdrawal {withdrawal_request.id}"
            )
            
            withdrawal_request.status = 'cancelled'
            withdrawal_request.save()
            
            return Response(
                WithdrawalRequestSerializer(withdrawal_request).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_stats(request):
    """Get wallet statistics"""
    
    wallet_service = WalletService()
    stats = wallet_service.get_wallet_stats(request.user)
    
    serializer = WalletStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_summary(request):
    """Get wallet summary"""
    
    user = request.user
    wallets = Wallet.objects.filter(user=user).select_related('cryptocurrency')
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        wallet__user=user
    ).select_related('wallet__cryptocurrency').order_by('-created_at')[:10]
    
    # Get pending withdrawals
    pending_withdrawals = WithdrawalRequest.objects.filter(
        user=user,
        status__in=['pending', 'approved', 'processing']
    ).select_related('cryptocurrency')
    
    return Response({
        'wallets': WalletSerializer(wallets, many=True).data,
        'recent_transactions': TransactionSerializer(recent_transactions, many=True).data,
        'pending_withdrawals': WithdrawalRequestSerializer(pending_withdrawals, many=True).data,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def simulate_deposit(request):
    """Simulate a deposit for testing purposes"""
    
    crypto_id = request.data.get('cryptocurrency_id')
    amount = request.data.get('amount')
    
    if not crypto_id or not amount:
        return Response(
            {'error': 'cryptocurrency_id و amount الزامی است'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        cryptocurrency = Cryptocurrency.objects.get(id=crypto_id, is_active=True)
        amount = Decimal(str(amount))
    except (Cryptocurrency.DoesNotExist, ValueError):
        return Response(
            {'error': 'اطلاعات نامعتبر'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create and confirm deposit
    wallet_service = WalletService()
    try:
        # Create deposit transaction
        transaction_obj = wallet_service.create_deposit_transaction(
            user=request.user,
            cryptocurrency=cryptocurrency,
            amount=amount,
            external_tx_id=f"test_{timezone.now().timestamp()}",
            from_address="test_address"
        )
        
        # Immediately confirm it for testing
        wallet_service.confirm_deposit(transaction_obj)
        
        return Response({
            'message': 'واریز شبیه‌سازی شده با موفقیت انجام شد',
            'transaction': TransactionSerializer(transaction_obj).data
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )