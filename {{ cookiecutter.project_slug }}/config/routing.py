from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.middleware import TokenMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
