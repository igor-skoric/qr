from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Image
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator


@login_required(login_url='/myadmin/login/')
def home(request):
    title = "Poslednja slika"
    context = {
        'title': title
    }

    return render(request, 'website/pages/index.html', context)


@login_required(login_url='/myadmin/login/')
def all_codes(request):
    images = Image.objects.all().order_by('-created_at')  # Svi objekti slika, sortirano po datumu kreiranja

    # Paginacija - 10 slika po stranici
    paginator = Paginator(images, 16)  # Broj slika po stranici
    page_number = request.GET.get('page')  # Broj stranice iz GET parametra
    page_obj = paginator.get_page(page_number)  # Dobijanje objekta za trenutnu stranicu

    context = {
        'page_obj': page_obj
    }

    return render(request, 'website/pages/all_codes.html', context)


@login_required(login_url='/myadmin/login/')
def code(request, pk):

    chosen_image = Image.objects.get(id=pk)
    title = "Izabrana slika iz liste slika"

    context = {
        'chosen_image': chosen_image,
        'title': title
    }
    print(context)
    return render(request, 'website/pages/index.html', context)


@login_required(login_url='/myadmin/login/')
def upload_image(request):
    context = {
        'images': 'images'
    }

    if request.POST:
        file = request.FILES.get('file')
        image = request.FILES['file']
        print(file)
        print(image)

    return render(request, 'website/pages/upload_image.html', context)


def image_upload(request):

    if request.method == 'POST' and request.FILES.get('file'):
        # Čuvanje slike u bazi podataka
        image = Image(image=request.FILES['file'])
        image.save()

        # Obavesti sve klijente preko WebSocket-a
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "qr_codes",
            {"type": "send_qr_code", "qr_code_url": image.qr_code},
        )


        # Vraćanje URL-a slike kao odgovora, koji će se koristiti u frontend-u
        image_url = image.image
        return JsonResponse({'file_url': image_url})

    return JsonResponse({'error': 'No image provided'}, status=400)

















