import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.room_group_name = f'stock_{self.product_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        pass  # We don't expect messages from client
    
    # Receive message from room group
    async def stock_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'product_id': event['product_id'],
            'stock': event['stock']
        }))
