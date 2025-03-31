from django.urls import re_path
from website import consumers

# Definiši WebSocket rutiranje
websocket_urlpatterns = [
    re_path(r'ws/somepath/$', consumers.ImageConsumer.as_asgi()),  # URL putanja za WebSocket
]
