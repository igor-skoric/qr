from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image, Client


admin.site.register(Image)



class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'background_image')  # Prikazivanje kolona u adminu
    list_filter = ('is_default',)  # Filter po defaultu
    search_fields = ('name',)  # Pretraga po nazivu projekta

admin.site.register(Client, ClientAdmin)
