from django.urls import re_path
from mqtt_topics.consumers import SensorWebSocketConsumer

websocket_urlpatterns = [
    re_path(r"^ws/sensor/temperature$", SensorWebSocketConsumer.as_asgi()),
]