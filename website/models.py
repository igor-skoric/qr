from django.db import models
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings


# Model za korisnika
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.email


# Model za sliku
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='user_images/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatsko ažuriranje prilikom svake izmene

    def save(self, *args, **kwargs):
        # Generisanje QR koda samo ako slika nije prazna
        if self.image:
            qr_code_image = self.generate_qr_code()
            self.qr_code = qr_code_image

        super().save(*args, **kwargs)

    def generate_qr_code(self):
        # Generisanje QR koda na osnovu URL-a slike
        qr_data = self.image.url
        qr = qrcode.make(qr_data)

        # Spremanje QR koda u memoriji
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)

        # Kreiranje InMemoryUploadedFile objekta za čuvanje QR koda u bazi
        qr_file = InMemoryUploadedFile(qr_io, None, 'qr_code.png', 'image/png', qr_io.tell(), None)

        return qr_file

    def __str__(self):
        return f"Slika korisnika {self.user.username} - QR kod"

    @classmethod
    def get_last_updated_image_for_user(cls, user):
        """
        Vraća poslednju ažuriranu sliku za korisnika
        """
        return cls.objects.filter(user=user).order_by('-updated_at').first()