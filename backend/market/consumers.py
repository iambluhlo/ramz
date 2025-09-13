import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MarketData
from trading.models import TradingPair, OrderBook, Trade

class MarketDataConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time market data"""
    
    async def connect(self):
        self.trading_pair_id = self.scope['url_route']['kwargs']['trading_pair_id']
        self.room_group_name = f'market_{self.trading_pair_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial market data
        market_data = await self.get_market_data()
        if market_data:
            await self.send(text_data=json.dumps({
                'type': 'market_data',
                'data': market_data
            }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        pass
    
    async def market_data_update(self, event):
        """Send market data update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'market_data',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_market_data(self):
        try:
            market_data = MarketData.objects.select_related(
                'trading_pair__base_currency', 'trading_pair__quote_currency'
            ).get(trading_pair_id=self.trading_pair_id)
            
            return {
                'trading_pair': market_data.trading_pair.symbol,
                'last_price': str(market_data.last_price),
                'bid_price': str(market_data.bid_price),
                'ask_price': str(market_data.ask_price),
                'high_24h': str(market_data.high_24h),
                'low_24h': str(market_data.low_24h),
                'volume_24h': str(market_data.volume_24h),
                'price_change_24h': str(market_data.price_change_24h),
                'price_change_percent_24h': str(market_data.price_change_percent_24h),
                'updated_at': market_data.updated_at.isoformat(),
            }
        except MarketData.DoesNotExist:
            return None


class OrderBookConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time order book data"""
    
    async def connect(self):
        self.trading_pair_id = self.scope['url_route']['kwargs']['trading_pair_id']
        self.room_group_name = f'orderbook_{self.trading_pair_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial order book
        order_book = await self.get_order_book()
        await self.send(text_data=json.dumps({
            'type': 'orderbook',
            'data': order_book
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        pass
    
    async def orderbook_update(self, event):
        """Send order book update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'orderbook',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_order_book(self):
        try:
            # Get bids and asks
            bids = list(OrderBook.objects.filter(
                trading_pair_id=self.trading_pair_id,
                side='buy'
            ).order_by('-price')[:20].values('price', 'quantity', 'order_count'))
            
            asks = list(OrderBook.objects.filter(
                trading_pair_id=self.trading_pair_id,
                side='sell'
            ).order_by('price')[:20].values('price', 'quantity', 'order_count'))
            
            # Convert Decimal to string for JSON serialization
            for bid in bids:
                bid['price'] = str(bid['price'])
                bid['quantity'] = str(bid['quantity'])
            
            for ask in asks:
                ask['price'] = str(ask['price'])
                ask['quantity'] = str(ask['quantity'])
            
            return {
                'bids': bids,
                'asks': asks,
            }
        except Exception as e:
            return {'bids': [], 'asks': []}


class TradesConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time trades"""
    
    async def connect(self):
        self.trading_pair_id = self.scope['url_route']['kwargs']['trading_pair_id']
        self.room_group_name = f'trades_{self.trading_pair_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send recent trades
        recent_trades = await self.get_recent_trades()
        await self.send(text_data=json.dumps({
            'type': 'trades',
            'data': recent_trades
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        pass
    
    async def trade_update(self, event):
        """Send new trade to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'trade',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_recent_trades(self):
        try:
            trades = list(Trade.objects.filter(
                trading_pair_id=self.trading_pair_id
            ).order_by('-created_at')[:50].values(
                'id', 'quantity', 'price', 'created_at'
            ))
            
            # Convert data for JSON serialization
            for trade in trades:
                trade['id'] = str(trade['id'])
                trade['quantity'] = str(trade['quantity'])
                trade['price'] = str(trade['price'])
                trade['created_at'] = trade['created_at'].isoformat()
            
            return trades
        except Exception as e:
            return []