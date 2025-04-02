import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Image
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# @receiver(post_delete, sender=Image)
# def delete_image_files(sender, instance, **kwargs):
#     """ Briše slike iz fajl sistema kada se model obriše iz baze. """
#
#     # Briše glavnu sliku
#     if instance.image:
#         image_path = instance.image.path
#         if os.path.isfile(image_path):
#             os.remove(image_path)
#
#     # Briše QR kod ako postoji
#     if instance.qr_code:
#         qr_code_path = instance.qr_code.path
#         if os.path.isfile(qr_code_path):
#             os.remove(qr_code_path)


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