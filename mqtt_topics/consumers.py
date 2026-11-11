import json
from channels.db import database_sync_to_async
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from mqttasgi.consumers import MqttConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Mesure

TOPIC = 'sensor/data'
GROUP_NAME = 'sensor_data'


class SensorWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data", self.channel_name)
        await self.accept()
        print("WS: client joined sensor_data")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(GROUP_NAME, self.channel_name)

    async def sensor_temperature(self, event):
        print("WS: got group message", event)
        data = json.loads(event["message"]["payload"])
        await self.send(text_data=json.dumps(data))


class GrandeurMqttConsumer(MqttConsumer):

    async def connect(self):
        # s'abonner au topic MQTT (QoS 2 = exactement une fois)
        await self.subscribe(TOPIC, 2)
        # rejoindre le group Redis
        self.room_group_name = GROUP_NAME
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print('MQTT connected....')

    async def receive(self, mqtt_message):
        print(">>> message MQTT reçu")
        topic = mqtt_message['topic']
        payload = mqtt_message['payload'].decode('utf-8', errors='replace')

        print(f"Received [{topic}] QoS {mqtt_message['qos']}: {payload}")

        # publier le message dans le group → dashboard + persistence le reçoivent
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "sensor.temperature",   # → appelle sensor_temperature()
                "message": {"topic": topic, "payload": payload},
            }
        )

    # Receive message from group → save to DB
    async def sensor_temperature(self, event):
        message = event["message"]
        data = None
        try:
            data = json.loads(message["payload"])
            mesure = await self.save_mesure(message["topic"], data)
            print(f"[DB] saved ✔ {mesure}")
        except Exception as e:
            print(f"[DB] ERROR: {e!r}")
        if data is not None:
            try:
                from persistence.persistence_engine import persist_mesure_firebase
                await persist_mesure_firebase(data)
            except Exception as e:
                print(f"[Firebase] ERROR: {e!r}")

    @database_sync_to_async
    def save_mesure(self, topic, data):
        date = parse_datetime(data.get("date_prise", "")) or timezone.now()
        return Mesure.objects.create(
            topic=topic,
            value=float(data["value"]),
            date_prise=date,
        )

    async def disconnect(self):
        await self.unsubscribe(TOPIC)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)