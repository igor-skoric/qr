from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image, Client


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'image', 'qr_code', 'created_at')
    ordering = ('-created_at',)

    # Dodavanje prilagođenog template-a za listu objekata
    change_list_template = 'admin/image_change_list.html'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" />')
        return 'No image'
    image_preview.short_description = 'Image Preview'


admin.site.register(Image, ImageAdmin)



class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'background_image')  # Prikazivanje kolona u adminu
    list_filter = ('is_default',)  # Filter po defaultu
    search_fields = ('name',)  # Pretraga po nazivu projekta

admin.site.register(Client, ClientAdmin)
