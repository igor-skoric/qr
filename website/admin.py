from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image


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
