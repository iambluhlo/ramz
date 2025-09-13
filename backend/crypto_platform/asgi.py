"""
ASGI config for crypto_platform project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import market.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_platform.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            market.routing.websocket_urlpatterns
        )
    ),
})