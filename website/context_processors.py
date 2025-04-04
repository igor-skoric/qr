from .models import Client, Image


def default_client(request):
    # Dohvati prvog klijenta sa is_default=True
    default_client = Client.objects.filter(is_default=True).first()
    return {'default_client': default_client}
