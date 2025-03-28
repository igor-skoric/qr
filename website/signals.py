from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import Image


@receiver(post_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    """ Briše slike iz fajl sistema kada se model obriše iz baze. """

    # Briše glavnu sliku
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)

    # Briše QR kod ako postoji
    if instance.qr_code:
        qr_code_path = instance.qr_code.path
        if os.path.isfile(qr_code_path):
            os.remove(qr_code_path)
