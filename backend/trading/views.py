from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Sum, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Cryptocurrency, TradingPair, Order, Trade, OrderBook, PriceHistory
from .serializers import (
    CryptocurrencySerializer, TradingPairSerializer, OrderSerializer,
    CreateOrderSerializer, TradeSerializer, OrderBookSerializer,
    PriceHistorySerializer, MarketStatsSerializer
)
from .services import OrderService


class CryptocurrencyListView(generics.ListAPIView):
    """List all active cryptocurrencies"""
    
    queryset = Cryptocurrency.objects.filter(is_active=True)
    serializer_class = CryptocurrencySerializer
    permission_classes = [permissions.AllowAny]


class TradingPairListView(generics.ListAPIView):
    """List all active trading pairs"""
    
    queryset = TradingPair.objects.filter(is_active=True).select_related(
        'base_currency', 'quote_currency'
    )
    serializer_class = TradingPairSerializer
    permission_classes = [permissions.AllowAny]


class CreateOrderView(generics.CreateAPIView):
    """Create a new order"""
    
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user can trade
        if not request.user.is_trading_enabled:
            return Response(
                {'error': 'معاملات برای حساب شما غیرفعال است'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create order using service
        order_service = OrderService()
        try:
            order = order_service.create_order(
                user=request.user,
                **serializer.validated_data
            )
            
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserOrdersView(generics.ListAPIView):
    """List user's orders"""
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).select_related(
            'trading_pair__base_currency', 'trading_pair__quote_currency'
        )
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by trading pair
        pair_filter = self.request.query_params.get('trading_pair')
        if pair_filter:
            queryset = queryset.filter(trading_pair_id=pair_filter)
        
        return queryset.order_by('-created_at')


class CancelOrderView(generics.UpdateAPIView):
    """Cancel an order"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'سفارش یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if order.status not in ['pending', 'partially_filled']:
            return Response(
                {'error': 'این سفارش قابل لغو نیست'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel order using service
        order_service = OrderService()
        try:
            order_service.cancel_order(order)
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserTradesView(generics.ListAPIView):
    """List user's trades"""
    
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_orders = Order.objects.filter(user=self.request.user)
        queryset = Trade.objects.filter(
            Q(maker_order__in=user_orders) | Q(taker_order__in=user_orders)
        ).select_related(
            'trading_pair__base_currency', 'trading_pair__quote_currency'
        )
        
        # Filter by trading pair
        pair_filter = self.request.query_params.get('trading_pair')
        if pair_filter:
            queryset = queryset.filter(trading_pair_id=pair_filter)
        
        return queryset.order_by('-created_at')


class OrderBookView(generics.ListAPIView):
    """Get order book for a trading pair"""
    
    serializer_class = OrderBookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        trading_pair_id = self.kwargs.get('trading_pair_id')
        return OrderBook.objects.filter(
            trading_pair_id=trading_pair_id
        ).order_by('side', '-price')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Separate bids and asks
        bids = queryset.filter(side='buy').order_by('-price')[:20]
        asks = queryset.filter(side='sell').order_by('price')[:20]
        
        return Response({
            'bids': OrderBookSerializer(bids, many=True).data,
            'asks': OrderBookSerializer(asks, many=True).data
        })


class RecentTradesView(generics.ListAPIView):
    """Get recent trades for a trading pair"""
    
    serializer_class = TradeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        trading_pair_id = self.kwargs.get('trading_pair_id')
        return Trade.objects.filter(
            trading_pair_id=trading_pair_id
        ).select_related(
            'trading_pair__base_currency', 'trading_pair__quote_currency'
        ).order_by('-created_at')[:50]


class PriceHistoryView(generics.ListAPIView):
    """Get price history for charts"""
    
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        trading_pair_id = self.kwargs.get('trading_pair_id')
        timeframe = self.request.query_params.get('timeframe', '1h')
        limit = int(self.request.query_params.get('limit', 100))
        
        return PriceHistory.objects.filter(
            trading_pair_id=trading_pair_id,
            timeframe=timeframe
        ).order_by('-timestamp')[:limit]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def market_stats(request):
    """Get market statistics for all trading pairs"""
    
    stats = []
    trading_pairs = TradingPair.objects.filter(is_active=True).select_related(
        'base_currency', 'quote_currency'
    )
    
    for pair in trading_pairs:
        # Get 24h stats
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        
        # Get recent trades
        recent_trades = Trade.objects.filter(
            trading_pair=pair,
            created_at__gte=yesterday
        )
        
        if recent_trades.exists():
            # Calculate stats
            last_trade = Trade.objects.filter(trading_pair=pair).order_by('-created_at').first()
            last_price = last_trade.price if last_trade else Decimal('0')
            
            # Get price 24h ago
            old_trade = Trade.objects.filter(
                trading_pair=pair,
                created_at__lte=yesterday
            ).order_by('-created_at').first()
            old_price = old_trade.price if old_trade else last_price
            
            price_change = last_price - old_price
            price_change_percent = (price_change / old_price * 100) if old_price > 0 else Decimal('0')
            
            # Volume and price stats
            volume_24h = recent_trades.aggregate(Sum('quantity'))['quantity__sum'] or Decimal('0')
            high_24h = recent_trades.aggregate(Max('price'))['price__max'] or last_price
            low_24h = recent_trades.aggregate(Min('price'))['price__min'] or last_price
            
            volume_24h_quote = sum(
                trade.quantity * trade.price for trade in recent_trades
            ) if recent_trades.exists() else Decimal('0')
            
        else:
            # No trades in 24h
            last_price = Decimal('0')
            price_change = Decimal('0')
            price_change_percent = Decimal('0')
            high_24h = Decimal('0')
            low_24h = Decimal('0')
            volume_24h = Decimal('0')
            volume_24h_quote = Decimal('0')
        
        stats.append({
            'symbol': pair.symbol,
            'last_price': last_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'high_24h': high_24h,
            'low_24h': low_24h,
            'volume_24h': volume_24h,
            'volume_24h_quote': volume_24h_quote,
        })
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def trading_stats(request):
    """Get user's trading statistics"""
    
    user = request.user
    
    # Get user's orders and trades
    user_orders = Order.objects.filter(user=user)
    user_trades = Trade.objects.filter(
        Q(maker_order__user=user) | Q(taker_order__user=user)
    )
    
    # Calculate stats
    total_orders = user_orders.count()
    filled_orders = user_orders.filter(status='filled').count()
    cancelled_orders = user_orders.filter(status='cancelled').count()
    
    total_trades = user_trades.count()
    total_volume = user_trades.aggregate(Sum('quantity'))['quantity__sum'] or Decimal('0')
    
    # Get recent activity
    recent_orders = user_orders.order_by('-created_at')[:5]
    recent_trades = user_trades.order_by('-created_at')[:5]
    
    return Response({
        'total_orders': total_orders,
        'filled_orders': filled_orders,
        'cancelled_orders': cancelled_orders,
        'total_trades': total_trades,
        'total_volume': total_volume,
        'recent_orders': OrderSerializer(recent_orders, many=True).data,
        'recent_trades': TradeSerializer(recent_trades, many=True).data,
    })