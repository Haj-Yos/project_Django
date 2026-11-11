from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'sensor_temperature'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()                           # without this, the client is refused
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    async def sensor_temperature(self, event):        # same event as in part 1
        data = json.loads(event["message"]["payload"])
        await self.send(text_data=json.dumps({
            "valeur": data.get("valeur", data.get("value")),
            "date_prise": data.get("date_prise"),
        }))       