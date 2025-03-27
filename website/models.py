from django.db import models
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sites.models import Site


class Image(models.Model):
    image = models.ImageField(upload_to='user_images/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Generisanje QR koda samo ako slika nije prazna

        if self.image:
            qr_code_image = self.generate_qr_code()
            self.qr_code.save(f"qr_{self.pk}.png", qr_code_image, save=False)  # Čuvamo QR kod
            super().save(update_fields=['qr_code'])  # Drugi put sačuvaj samo `qr_code`


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