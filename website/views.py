from django.shortcuts import render, get_object_or_404
from .models import Image
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login/')
def home(request):

    last_image = Image.objects.all().order_by('-created_at').first()
    title = "Poslednja slika"
    context = {
        'last_image': last_image,
        'title': title
    }

    return render(request, 'website/pages/index.html', context)


@login_required(login_url='/admin/login/')
def all_codes(request):

    images = Image.objects.all().order_by('-created_at')

    context = {
        'images': images
    }

    return render(request, 'website/pages/all_codes.html', context)


@login_required(login_url='/admin/login/')
def code(request, pk):

    last_image = Image.objects.get(id=pk)
    title = "Izabrana slika iz liste slika"

    context = {
        'last_image': last_image,
        'title': title
    }

    return render(request, 'website/pages/index.html', context)