import os
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from .models import Image, Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Image)
def notify_new_image(sender, instance, created, **kwargs):
    if instance.qr_code:
        # Kada je nova slika kreirana i QR kod je sačuvan
        channel_layer = get_channel_layer()

        # Šaljemo poruku svim korisnicima u grupi "image_group"
        async_to_sync(channel_layer.group_send)(
            "image_group",  # Grupa kojoj šaljemo poruku
            {
                "type": "new_image",  # Tip poruke koji želimo da obradimo
                "message": instance.qr_code  # URL nove slike
            }
        )

# Signal koji se aktivira pre nego što objekat bude obrisan iz baze
@receiver(pre_delete, sender=Image)
def delete_image_from_cloudinary(sender, instance, **kwargs):
    # Briše slike sa Cloudinary-ja kada se objekat obriše iz baze
    logger.info(f"Usao u delete sa Cloudinary-ja {instance}")
    image_public_id = get_public_id_from_url(instance.image.public_id)
    qr_public_id = get_public_id_from_url(instance.qr_code.public_id)

    if image_public_id:
        cloudinary.uploader.destroy(image_public_id)
    if qr_public_id:
        cloudinary.uploader.destroy(qr_public_id)


@receiver(pre_delete, sender=Client)
def delete_client_from_cloudinary(sender, instance, **kwargs):
    logger.info(f"Usao u delete sa Cloudinary-ja {instance}")
    # Briše slike sa Cloudinary-ja kada se objekat obriše iz baze
    background_image_public_id = get_public_id_from_url(instance.background_image.public_id)

    if background_image_public_id:
        y = cloudinary.uploader.destroy(background_image_public_id)

def get_public_id_from_url(url):
    # Splitujemo URL kod '/upload/'
    logger.info(f"Usao u get_public_id_from_url ")
    split_url = url.split('/upload/')
    if len(split_url) == 2:
        # Drugi deo je ono što nas zanima, delimo ga opet
        version_and_public_id = split_url[1].split('/', 1)  # Delimo na verziju i public_id
        if len(version_and_public_id) == 2:
            public_id = version_and_public_id[1]  # Drugi deo je public_id
            return public_id
    return None  # Ako nije u ispravnom formatu