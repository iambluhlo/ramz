from django.urls import path
from . import views

urlpatterns = [
    # Wallets
    path('', views.UserWalletsView.as_view(), name='user_wallets'),
    path('summary/', views.wallet_summary, name='wallet_summary'),
    path('stats/', views.wallet_stats, name='wallet_stats'),
    
    # Transactions
    path('transactions/', views.UserTransactionsView.as_view(), name='user_transactions'),
    
    # Deposits
    path('deposit-address/<int:crypto_id>/', views.DepositAddressView.as_view(), name='deposit_address'),
    path('simulate-deposit/', views.simulate_deposit, name='simulate_deposit'),
    
    # Withdrawals
    path('withdraw/', views.CreateWithdrawalView.as_view(), name='create_withdrawal'),
    path('withdrawals/', views.UserWithdrawalsView.as_view(), name='user_withdrawals'),
    path('withdrawals/<uuid:withdrawal_id>/cancel/', views.CancelWithdrawalView.as_view(), name='cancel_withdrawal'),
]