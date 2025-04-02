from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image, Client


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image', 'qr_code', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Image, ImageAdmin)



class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'background_image')  # Prikazivanje kolona u adminu
    list_filter = ('is_default',)  # Filter po defaultu
    search_fields = ('name',)  # Pretraga po nazivu projekta

admin.site.register(Client, ClientAdmin)
