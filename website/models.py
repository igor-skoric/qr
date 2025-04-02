import qrcode
import os
from django.db import models
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sites.models import Site
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
import cloudinary.uploader

class Image(models.Model):
    image = CloudinaryField()
    qr_code = CloudinaryField()
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Prvo sačuvaj objekat, kako bi mogao da dobiješ URL slike
        super().save(*args, **kwargs)

        # Generisanje QR koda samo ako slika postoji i QR kod nije već postavljen
        if self.image and not self.qr_code:
            image_url = self.image.url  # Dobij URL slike sa Cloudinary-ja

            qr_code_image = self.generate_qr_code(image_url)  # Generiši QR kod sa URL-om slike

            # Sačuvaj QR kod u memoriji
            qr_code_image_file = BytesIO()
            qr_code_image.save(qr_code_image_file, format='PNG')
            qr_code_image_file.seek(0)  # Resetuj pokazivač na početak

            # Učitavanje QR koda na Cloudinary
            result = cloudinary.uploader.upload(qr_code_image_file, public_id=f"qr_{self.pk}", resource_type="image")

            # Čuvanje URL-a generisanog QR koda
            self.qr_code = result['secure_url']
            super().save(update_fields=['qr_code'])

    def generate_qr_code(self, data):
        """Generiše QR kod sa prosleđenim URL-om slike."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)  # Koristi URL slike kao sadržaj QR koda
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        return img

    def __str__(self):
        return f"Image {self.id}"


    def __str__(self):
        return f"Image {self.id}"


class Client(models.Model):
    name = models.CharField(max_length=100)  # Naziv projekta
    background_image = CloudinaryField()  # Slika pozadine
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