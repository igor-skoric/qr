from django.shortcuts import render, get_object_or_404
from .models import Image, User


# View za prikaz slike i njenog QR koda
def home(request, user_id = 1):

    # Dobijanje slike na osnovu njenog ID-a
    user = get_object_or_404(User, id=user_id)

    # Dobijanje poslednje ažurirane slike korisnika
    image = Image.get_last_updated_image_for_user(user)
    images = Image.objects.all()
    # Kreiraj context sa URL-ovima za sliku i njen QR kod
    context = {
        'images': images,
        # 'image_url': image.image.url,  # URL slike
        # 'qr_code_url': image.qr_code.url,  # URL QR koda
    }

    return render(request, 'website/pages/index.html', context)
