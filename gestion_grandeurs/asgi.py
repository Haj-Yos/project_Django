"""
ASGI config for gestion_grandeurs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_grandeurs.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from dashboard.routing import websocket_urlpatterns
from mqtt_topics.consumers import GrandeurMqttConsumer


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': GrandeurMqttConsumer.as_asgi(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})