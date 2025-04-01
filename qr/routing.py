from website.consumers import ImageConsumer
from django.urls import re_path

# Definiši WebSocket rutiranje
websocket_urlpatterns = [
    re_path(r'ws/somepath/$', ImageConsumer.as_asgi()),  # URL putanja za WebSocket
]
