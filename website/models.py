import qrcode
import os
from django.db import models
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sites.models import Site
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

class Image(models.Model):
    image = models.CloudinaryField(upload_to='user_images/')
    qr_code = models.CloudinaryField(upload_to='qr_codes/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Prvo sačuvaj objekat, kako bi mogao da dobiješ ID
        super().save(*args, **kwargs)

        # Generisanje QR koda samo ako slika postoji
        if self.image and not self.qr_code:
            qr_code_image = self.generate_qr_code()
            self.qr_code.save(f"qr_{self.pk}.png", qr_code_image, save=False)

            # Sačuvaj samo qr_code
            super().save(update_fields=['qr_code'])


    def generate_qr_code(self):
        # Dobijanje domena aplikacije
        domain = Site.objects.get_current().domain
        # Generisanje apsolutnog URL-a slike
        qr_data = f"https://{domain}{self.image.url}"

        # Generisanje QR koda
        qr = qrcode.make(qr_data)

        # Spremanje QR koda u memoriji
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)

        # Kreiranje InMemoryUploadedFile objekta za čuvanje QR koda u bazi
        qr_file = InMemoryUploadedFile(qr_io, None, 'qr_code.png', 'image/png', qr_io.tell(), None)

        return qr_file


    def __str__(self):
        return f"Image {self.id}"


class Client(models.Model):
    name = models.CharField(max_length=100)  # Naziv projekta
    background_image = models.ImageField(upload_to='client_backgrounds/')  # Slika pozadine
    is_default = models.BooleanField(default=False)  # Da li je ovo podrazumevana slika pozadine

    def save(self, *args, **kwargs):
        # Ako je označen kao default, postavi sve druge is_default na False
        if self.is_default:
            Client.objects.exclude(id=self.id).update(is_default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):

    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)

    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)