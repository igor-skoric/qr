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
    image = CloudinaryField()
    qr_code = CloudinaryField()
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Prvo sačuvaj objekat, kako bi mogao da dobiješ ID
        super().save(*args, **kwargs)

        # Generisanje QR koda samo ako slika postoji i QR kod nije već postavljen
        if self.image and not self.qr_code:
            qr_code_image = self.generate_qr_code()

            # Sačuvaj generisani QR kod na Cloudinary
            qr_code_image_file = BytesIO()
            qr_code_image.save(qr_code_image_file, format='PNG')
            qr_code_image_file.seek(0)  # Vratiti pokazivač na početak datoteke

            # Učitavanje slike na Cloudinary
            result = cloudinary.uploader.upload(qr_code_image_file, public_id=f"qr_{self.pk}", resource_type="image")

            # Dodavanje URL-a sačuvane slike u qr_code polje
            self.qr_code = result['secure_url']

            # Sačuvaj samo qr_code
            super().save(update_fields=['qr_code'])

    def generate_qr_code(self):
        # Ovaj metod treba da generiše QR kod na osnovu `self.image` ili drugih podataka
        import qrcode
        qr = qrcode.make("Some data related to the image or model")
        return qr  # Vraća PIL Image objekat


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