import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from qr.routing import websocket_urlpatterns  # Dodaj ovaj import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qr.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # Ovdje koristiš websocket_urlpatterns
    ),
})
