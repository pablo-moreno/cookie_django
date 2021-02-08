from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from chat.consumers import ChatConsumer
from utils.channels.middleware import TokenMiddleware


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenMiddleware(
        URLRouter([
            path('ws/chat/', ChatConsumer),
        ])
    )
})
