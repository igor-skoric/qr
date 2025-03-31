import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Image, Client
from channels.db import database_sync_to_async


class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "image_group"

        # Dodavanje korisnika u grupu
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Prihvatanje WebSocket konekcije
        await self.accept()

        # Pošaljite poslednju sliku odmah prilikom konekcije
        latest_image = await self.get_latest_image()

        if latest_image:
            image_url = latest_image.qr_code.url
        else:
            default_client = await self.get_default_client()
            image_url = default_client.background_image.url



        await self.send(text_data=json.dumps({
            'message': image_url  # Pošaljite samo URL slike
        }))

    async def disconnect(self, close_code):
        # Uklanjanje korisnika iz grupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Obrada novih slika koja stiže kroz signal
    async def new_image(self, event):
        # Kada signal stigne, pošaljemo URL nove slike svim korisnicima
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    from channels.db import database_sync_to_async

    @database_sync_to_async
    def get_latest_image(self):
        try:
            # Pokušavamo da dohvatimo poslednju sliku prema `created_at`
            return Image.objects.latest('created_at')
        except Image.DoesNotExist:
            # Ako nema slika, vraćamo None
            return None

    # Funkcija za dohvat default klijenta
    @database_sync_to_async
    def get_default_client(self):
        return Client.objects.filter(is_default=True).first()