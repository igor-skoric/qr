from django.contrib import admin
from .models import Image, Client
from django.contrib.admin import AdminSite, DateFieldListFilter


class MyAdminSite(AdminSite):
    site_header = "My Custom Admin"
    index_title = "Welcome to My Admin Panel"


# Instanca prilagođenog admin panela
admin_site = MyAdminSite(name='myadmin')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'qr_code', 'created_at')
    search_fields = ('created_at',)  # Pretraga samo po datumu
    readonly_fields = ('qr_code',)

    # Dodaj filtriranje za datum
    list_filter = (
        ('created_at', DateFieldListFilter),
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'background_image')  # Prikazivanje kolona u adminu
    list_filter = ('is_default',)  # Filter po defaultu
    search_fields = ('name',)  # Pretraga po nazivu projekta
    readonly_fields = ('slug',)


admin_site.register(Image, ImageAdmin)
admin_site.register(Client, ClientAdmin)
