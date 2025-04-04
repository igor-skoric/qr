import qrcode
import os
from django.db import models
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sites.models import Site
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField, CloudinaryResource
import cloudinary.uploader
from django.utils.text import slugify

class Image(models.Model):
    image = CloudinaryField()
    qr_code = CloudinaryField()
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Pre upload-a, obavezno transformišite sliku u WebP
        if self.image:
            # Za sliku, postavite transformaciju u WebP format prilikom upload-a
            transformed_image = cloudinary.uploader.upload(
                self.image,
                format="webp",  # Postavite WebP format
                folder=self.get_client_path(),
                quality="auto",  # Automatska optimizacija kvaliteta
                resource_type="image"
            )
            self.image = transformed_image['secure_url']  # Sačuvaj transformisanu URL sliku

        # Prvo sačuvaj objekat, kako bi mogao da dobiješ URL slike
        super().save(*args, **kwargs)

        # Generisanje QR koda samo ako slika postoji i QR kod nije već postavljen
        if self.image and not self.qr_code:
            image_url = self.image  # Koristi URL transformisane slike

            if not image_url:
                return  # Ako nema URL-a za sliku, izlazi iz metode

            qr_code_image = self.generate_qr_code(image_url)  # Generiši QR kod sa URL-om slike

            # Sačuvaj QR kod u memoriji
            qr_code_image_file = BytesIO()
            qr_code_image.save(qr_code_image_file, format='PNG')
            qr_code_image_file.seek(0)  # Resetuj pokazivač na početak

            try:
                # Učitavanje QR koda na Cloudinary sa WebP formatom i automatskom optimizacijom
                result = cloudinary.uploader.upload(qr_code_image_file, public_id=f"qr_{self.pk}", resource_type="image", format="webp", folder=self.get_client_path(), quality="auto")

                # Čuvanje URL-a generisanog QR koda
                self.qr_code = result['secure_url']
                super().save(update_fields=['qr_code'])  # Sačuvaj samo QR kod u bazi
            except cloudinary.exceptions.Error as e:
                # Obrada greške u slučaju neuspelog upload-a
                print(f"Error uploading QR code to Cloudinary: {e}")
                # Možete dodati neki fallback mehanizam ili zapisati grešku

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

    def get_client_path(self):
        path = 'clients/default'
        client = Client.objects.filter(is_default=True).first()
        if client:
            path = f'clients/{client.slug}/'
        return path
    def __str__(self):
        return f"Image {self.id}"


class Client(models.Model):
    name = models.CharField(max_length=100)  # Naziv projekta
    background_image = CloudinaryField(max_length=255)  # Slika pozadine
    is_default = models.BooleanField(default=False)  # Da li je ovo podrazumevana slika pozadine
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        # Ako je označen kao default, postavi sve druge is_default na False
        if self.is_default:
            Client.objects.exclude(id=self.id).update(is_default=False)

        if not self.slug:
            self.slug = slugify(self.name)

        # Ako je instanca Cloudinary Resource onda ne salji sliku
        if self.background_image and not isinstance(self.background_image, CloudinaryResource):
            # Za sliku, postavite transformaciju u WebP format prilikom upload-a

            transformed_image = cloudinary.uploader.upload(
                self.background_image,
                format="webp",  # Postavite WebP format
                folder="clients/background/",
                quality="auto",  # Automatska optimizacija kvaliteta
                resource_type="image"
            )

            self.background_image = transformed_image['secure_url']  # Sačuvaj transformisanu URL sliku

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.background_image)
