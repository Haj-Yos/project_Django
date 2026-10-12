from channels.generic.websocket import AsyncWebsocketConsumer
import json
class DashboardConsumer (AsyncWebsocketConsumer):
    async def connect(self):
        print('connect....')
        await self.accept()
        await self.send(text_data=json.dumps({"message": 'connected...'}))
    async def receive(self,mqtt_messsage):
        pass
    async def disconnect(self,close_code):
        pass        