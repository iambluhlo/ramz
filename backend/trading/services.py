from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Order, Trade, OrderBook, TradingPair
from wallet.services import WalletService

class OrderService:
    """Service for handling order operations"""
    
    def __init__(self):
        self.wallet_service = WalletService()
    
    def create_order(self, user, trading_pair, order_type, side, quantity, price=None, stop_price=None):
        """Create a new order"""
        
        with transaction.atomic():
            # Validate and reserve funds
            self._validate_and_reserve_funds(user, trading_pair, side, quantity, price)
            
            # Create order
            order = Order.objects.create(
                user=user,
                trading_pair=trading_pair,
                order_type=order_type,
                side=side,
                quantity=quantity,
                price=price,
                stop_price=stop_price,
                remaining_quantity=quantity
            )
            
            # Try to match order immediately for market orders
            if order_type == 'market':
                self._match_market_order(order)
            elif order_type == 'limit':
                self._match_limit_order(order)
            
            return order
    
    def cancel_order(self, order):
        """Cancel an existing order"""
        
        with transaction.atomic():
            if order.status not in ['pending', 'partially_filled']:
                raise ValueError("سفارش قابل لغو نیست")
            
            # Release reserved funds
            self._release_reserved_funds(order)
            
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            # Update order book
            self._update_order_book(order.trading_pair)
    
    def _validate_and_reserve_funds(self, user, trading_pair, side, quantity, price):
        """Validate user has sufficient funds and reserve them"""
        
        if side == 'buy':
            # For buy orders, need quote currency
            currency = trading_pair.quote_currency
            if price:
                required_amount = quantity * price
            else:
                # For market orders, estimate based on current market price
                last_trade = Trade.objects.filter(
                    trading_pair=trading_pair
                ).order_by('-created_at').first()
                if not last_trade:
                    raise ValueError("قیمت بازار موجود نیست")
                required_amount = quantity * last_trade.price * Decimal('1.01')  # 1% buffer
        else:
            # For sell orders, need base currency
            currency = trading_pair.base_currency
            required_amount = quantity
        
        # Check and reserve funds
        if not self.wallet_service.has_sufficient_balance(user, currency, required_amount):
            raise ValueError("موجودی کافی نیست")
        
        self.wallet_service.reserve_funds(user, currency, required_amount, f"Order reservation")
    
    def _release_reserved_funds(self, order):
        """Release reserved funds when order is cancelled"""
        
        if order.side == 'buy':
            currency = order.trading_pair.quote_currency
            if order.price:
                amount = order.remaining_quantity * order.price
            else:
                # Calculate based on average fill price or market price
                amount = order.remaining_quantity * order.price if order.price else Decimal('0')
        else:
            currency = order.trading_pair.base_currency
            amount = order.remaining_quantity
        
        if amount > 0:
            self.wallet_service.release_reserved_funds(
                order.user, currency, amount, f"Order {order.id} cancelled"
            )
    
    def _match_market_order(self, order):
        """Match a market order against existing orders"""
        
        opposite_side = 'sell' if order.side == 'buy' else 'buy'
        
        # Get matching orders from order book
        if order.side == 'buy':
            matching_orders = Order.objects.filter(
                trading_pair=order.trading_pair,
                side=opposite_side,
                status__in=['pending', 'partially_filled'],
                order_type='limit'
            ).order_by('price', 'created_at')
        else:
            matching_orders = Order.objects.filter(
                trading_pair=order.trading_pair,
                side=opposite_side,
                status__in=['pending', 'partially_filled'],
                order_type='limit'
            ).order_by('-price', 'created_at')
        
        remaining_quantity = order.remaining_quantity
        
        for matching_order in matching_orders:
            if remaining_quantity <= 0:
                break
            
            # Calculate trade quantity
            trade_quantity = min(remaining_quantity, matching_order.remaining_quantity)
            trade_price = matching_order.price
            
            # Execute trade
            self._execute_trade(order, matching_order, trade_quantity, trade_price)
            
            remaining_quantity -= trade_quantity
        
        # Update order status
        if remaining_quantity <= 0:
            order.status = 'filled'
        elif remaining_quantity < order.quantity:
            order.status = 'partially_filled'
        else:
            order.status = 'rejected'  # No matching orders found
        
        order.remaining_quantity = remaining_quantity
        order.save()
    
    def _match_limit_order(self, order):
        """Match a limit order against existing orders"""
        
        opposite_side = 'sell' if order.side == 'buy' else 'buy'
        
        # Get matching orders
        if order.side == 'buy':
            # Buy order matches with sell orders at or below the buy price
            matching_orders = Order.objects.filter(
                trading_pair=order.trading_pair,
                side=opposite_side,
                status__in=['pending', 'partially_filled'],
                order_type='limit',
                price__lte=order.price
            ).order_by('price', 'created_at')
        else:
            # Sell order matches with buy orders at or above the sell price
            matching_orders = Order.objects.filter(
                trading_pair=order.trading_pair,
                side=opposite_side,
                status__in=['pending', 'partially_filled'],
                order_type='limit',
                price__gte=order.price
            ).order_by('-price', 'created_at')
        
        remaining_quantity = order.remaining_quantity
        
        for matching_order in matching_orders:
            if remaining_quantity <= 0:
                break
            
            trade_quantity = min(remaining_quantity, matching_order.remaining_quantity)
            trade_price = matching_order.price  # Use maker's price
            
            self._execute_trade(matching_order, order, trade_quantity, trade_price)
            
            remaining_quantity -= trade_quantity
        
        # Update order status
        if remaining_quantity <= 0:
            order.status = 'filled'
        elif remaining_quantity < order.quantity:
            order.status = 'partially_filled'
        
        order.remaining_quantity = remaining_quantity
        order.save()
        
        # Add to order book if not fully filled
        if order.status in ['pending', 'partially_filled']:
            self._update_order_book(order.trading_pair)
    
    def _execute_trade(self, maker_order, taker_order, quantity, price):
        """Execute a trade between two orders"""
        
        # Calculate fees
        maker_fee = quantity * price * maker_order.trading_pair.base_currency.maker_fee
        taker_fee = quantity * price * taker_order.trading_pair.base_currency.taker_fee
        
        # Create trade record
        trade = Trade.objects.create(
            trading_pair=maker_order.trading_pair,
            maker_order=maker_order,
            taker_order=taker_order,
            quantity=quantity,
            price=price,
            maker_fee=maker_fee,
            taker_fee=taker_fee
        )
        
        # Update order quantities
        maker_order.filled_quantity += quantity
        maker_order.remaining_quantity -= quantity
        maker_order.fee += maker_fee
        
        taker_order.filled_quantity += quantity
        taker_order.remaining_quantity -= quantity
        taker_order.fee += taker_fee
        
        # Update order statuses
        if maker_order.remaining_quantity <= 0:
            maker_order.status = 'filled'
            maker_order.executed_at = timezone.now()
        elif maker_order.filled_quantity > 0:
            maker_order.status = 'partially_filled'
        
        if taker_order.remaining_quantity <= 0:
            taker_order.status = 'filled'
            taker_order.executed_at = timezone.now()
        elif taker_order.filled_quantity > 0:
            taker_order.status = 'partially_filled'
        
        maker_order.save()
        taker_order.save()
        
        # Update wallets
        self._update_wallets_after_trade(trade)
        
        return trade
    
    def _update_wallets_after_trade(self, trade):
        """Update user wallets after a trade"""
        
        base_currency = trade.trading_pair.base_currency
        quote_currency = trade.trading_pair.quote_currency
        
        # Maker gets base currency (if selling) or gives base currency (if buying)
        # Taker gives base currency (if buying) or gets base currency (if selling)
        
        if trade.maker_order.side == 'sell':
            # Maker sells base currency, gets quote currency
            self.wallet_service.transfer_funds(
                trade.maker_order.user, base_currency, -trade.quantity,
                f"Trade {trade.id} - Sell {base_currency.symbol}"
            )
            self.wallet_service.transfer_funds(
                trade.maker_order.user, quote_currency, 
                trade.quantity * trade.price - trade.maker_fee,
                f"Trade {trade.id} - Receive {quote_currency.symbol}"
            )
            
            # Taker buys base currency, gives quote currency
            self.wallet_service.transfer_funds(
                trade.taker_order.user, base_currency, trade.quantity,
                f"Trade {trade.id} - Buy {base_currency.symbol}"
            )
            self.wallet_service.transfer_funds(
                trade.taker_order.user, quote_currency, 
                -(trade.quantity * trade.price + trade.taker_fee),
                f"Trade {trade.id} - Pay {quote_currency.symbol}"
            )
        else:
            # Maker buys base currency, gives quote currency
            self.wallet_service.transfer_funds(
                trade.maker_order.user, base_currency, trade.quantity,
                f"Trade {trade.id} - Buy {base_currency.symbol}"
            )
            self.wallet_service.transfer_funds(
                trade.maker_order.user, quote_currency, 
                -(trade.quantity * trade.price + trade.maker_fee),
                f"Trade {trade.id} - Pay {quote_currency.symbol}"
            )
            
            # Taker sells base currency, gets quote currency
            self.wallet_service.transfer_funds(
                trade.taker_order.user, base_currency, -trade.quantity,
                f"Trade {trade.id} - Sell {base_currency.symbol}"
            )
            self.wallet_service.transfer_funds(
                trade.taker_order.user, quote_currency, 
                trade.quantity * trade.price - trade.taker_fee,
                f"Trade {trade.id} - Receive {quote_currency.symbol}"
            )
    
    def _update_order_book(self, trading_pair):
        """Update order book aggregated data"""
        
        # Clear existing order book data
        OrderBook.objects.filter(trading_pair=trading_pair).delete()
        
        # Aggregate pending orders by price and side
        pending_orders = Order.objects.filter(
            trading_pair=trading_pair,
            status__in=['pending', 'partially_filled'],
            order_type='limit'
        )
        
        # Group by side and price
        from django.db.models import Sum, Count
        
        aggregated_orders = pending_orders.values('side', 'price').annotate(
            total_quantity=Sum('remaining_quantity'),
            order_count=Count('id')
        )
        
        # Create order book entries
        for order_data in aggregated_orders:
            OrderBook.objects.create(
                trading_pair=trading_pair,
                side=order_data['side'],
                price=order_data['price'],
                quantity=order_data['total_quantity'],
                order_count=order_data['order_count']
            )