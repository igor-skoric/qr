from django.contrib import admin
from .models import User, Image

# Admin panel za User model

class UserAdmin(admin.ModelAdmin):
    # Omogućavamo pretragu po poljima
    search_fields = ['username', 'email']
    list_display = ('username', 'email')
    list_filter = ('email',)  # Filtriranje po emailu, po potrebi možeš dodati i druge filtre

admin.site.register(User, UserAdmin)


# Admin panel za Image model
class ImageAdmin(admin.ModelAdmin):
    # Omogućavamo pretragu po korisniku
    search_fields = ['user__username', 'user__email', 'updated_at']

    # Prikazujemo slike u listi admin panela
    list_display = ('user', 'image', 'qr_code', 'updated_at')

    # Omogućavamo filtriranje po korisniku i datumu ažuriranja
    list_filter = ('user', 'updated_at')


admin.site.register(Image, ImageAdmin)
